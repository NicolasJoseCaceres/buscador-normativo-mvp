import streamlit as st
import pandas as pd
from datetime import datetime
from dateutil import parser
from utils import match_query, highlight

st.set_page_config(page_title="Buscador Normativo Ambiental", layout="wide")

st.title("🔎 Buscador Normativo Ambiental / Administrativo")
st.caption("MVP – Carga desde CSV (editable) • Filtrá por jurisdicción, sector y tema • Búsqueda por palabras")

# Load data
@st.cache_data
def load_data(csv_path: str):
    df = pd.read_csv(csv_path, dtype=str).fillna("")
    # Normalize date
    def parse_date_safe(s):
        try:
            return parser.parse(s).date()
        except Exception:
            return None
    df["fecha_dt"] = df["fecha"].apply(parse_date_safe)
    return df

DATA_PATH = "data/normas.csv"
df = load_data(DATA_PATH)

with st.sidebar:
    st.subheader("Filtros")
    q = st.text_input("Palabras clave", placeholder="ej.: agua permisos perforación")
    jurisdicciones = sorted([j for j in df["jurisdiccion"].unique() if j])
    sectores = sorted([s for s in df["sector"].unique() if s])
    temas = sorted([t for t in df["tema"].unique() if t])

    sel_j = st.multiselect("Jurisdicción", jurisdicciones)
    sel_s = st.multiselect("Sector", sectores)
    sel_t = st.multiselect("Tema", temas)

    st.markdown("---")
    st.caption("⚙️ Datos")
    uploaded = st.file_uploader("Subir CSV propio (mismas columnas)", type=["csv"])
    if uploaded is not None:
        try:
            df_up = pd.read_csv(uploaded, dtype=str).fillna("")
            missing = set(df.columns) - set(df_up.columns)
            if missing:
                st.error(f"Faltan columnas en tu CSV: {', '.join(sorted(missing))}")
            else:
                df = df_up.copy()
                st.success("Datos cargados temporalmente. (No se guardan en el servidor del MVP)")
        except Exception as e:
            st.error(f"Error leyendo CSV: {e}")

    st.markdown("---")
    sort_by_date = st.toggle("Ordenar por fecha (desc)", value=True)
    page_size = st.slider("Resultados por página", 5, 50, 10, 5)

# Apply filters
mask = df.apply(lambda r: match_query(r.to_dict(), q), axis=1)
if sel_j:
    mask = mask & df["jurisdiccion"].isin(sel_j)
if sel_s:
    mask = mask & df["sector"].isin(sel_s)
if sel_t:
    mask = mask & df["tema"].isin(sel_t)

res = df[mask].copy()

if sort_by_date and "fecha_dt" in res.columns:
    res = res.sort_values("fecha_dt", ascending=False, na_position="last")

st.write(f"**{len(res)} resultados**")

# Pagination
page = st.number_input("Página", min_value=1, max_value=max(1, (len(res)-1)//page_size + 1), value=1, step=1)
start = (page-1)*page_size
end = start + page_size
page_df = res.iloc[start:end]

def fmt(x): 
    return "" if pd.isna(x) else str(x)

for _, row in page_df.iterrows():
    with st.container(border=True):
        st.markdown(f"### {fmt(row['norma'])} • {fmt(row['jurisdiccion'])} – {fmt(row['organismo'])}")
        sub = f"📅 {fmt(row['fecha'])} | 🏷️ {fmt(row['sector'])} • {fmt(row['tema'])} | 📌 {fmt(row['articulo'])}"
        st.markdown(sub)
        st.markdown(highlight(fmt(row['obligacion']), q), unsafe_allow_html=True)
        col1, col2 = st.columns([3,1])
        with col1:
            st.markdown(f"**Palabras clave:** {fmt(row['palabras_clave'])}")
            st.markdown(f"**Estado:** {fmt(row['estado'])}")
        with col2:
            if row.get("enlace_fuente"):
                st.link_button("Ver fuente", row["enlace_fuente"])

st.markdown("---")
st.caption("💡 Tip: podés embeber esta app en Carrd con un `<iframe>` y usar Google Sheets para alimentar el CSV.")
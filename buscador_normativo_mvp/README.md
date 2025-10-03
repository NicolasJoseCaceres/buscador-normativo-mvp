# Buscador Normativo Ambiental – MVP

## Requisitos
- Python 3.10+
- `pip install -r requirements.txt`

## Ejecutar local
```bash
streamlit run app.py
```

## Estructura
```
buscador_normativo_mvp/
├─ app.py
├─ utils.py
├─ requirements.txt
├─ .streamlit/config.toml
├─ data/normas.csv
└─ pages/Acerca.py
```

## Deploy (Streamlit Community Cloud)
1. Subí esta carpeta a un repo en GitHub.
2. Entra a https://share.streamlit.io/ y conectá tu repo.
3. Seleccioná `app.py` como archivo principal.
4. Cuando tengas la URL pública, embevela en Carrd con:
```html
<iframe src="https://TU-APP.streamlit.app" style="width:100%;height:90vh;border:0;"></iframe>
```

## CSV esperado
Columnas: `id,jurisdiccion,organismo,norma,fecha,sector,tema,articulo,obligacion,palabras_clave,enlace_fuente,estado`
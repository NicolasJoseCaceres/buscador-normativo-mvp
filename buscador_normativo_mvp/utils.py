from typing import List
import re

def tokenize(text: str) -> List[str]:
    if not text:
        return []
    return re.findall(r"\w+", text.lower(), flags=re.UNICODE)

def match_query(record: dict, q: str) -> bool:
    if not q:
        return True
    needles = tokenize(q)
    hay = " ".join([str(v) for v in record.values() if v is not None]).lower()
    return all(n in hay for n in needles)

def highlight(text: str, q: str) -> str:
    if not q or not text:
        return text or ""
    for token in set(tokenize(q)):
        text = re.sub(f"(?i)({re.escape(token)})", r"**\1**", text)
    return text
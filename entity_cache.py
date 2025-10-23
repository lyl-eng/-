# src/entity_cache.py

import spacy
import json
from pathlib import Path

CACHE_PATH = Path("data/entity_cache.json")

nlp = spacy.load("en_core_web_sm")  # 英文实体识别

def extract_entities(text: str) -> list[str]:
    doc = nlp(text)
    return list(set(ent.text for ent in doc.ents))

def load_entity_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}

def save_entity_cache(entity_map: dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(entity_map, ensure_ascii=False, indent=2), encoding="utf-8")

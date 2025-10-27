# src/entity_cache.py

import spacy
import json
from pathlib import Path

CACHE_PATH = Path("data/entity_cache.json")

nlp = spacy.load("en_core_web_sm")  # 英文实体识别

# def extract_entities(text: str) -> list[str]:
#     doc = nlp(text)
#     return list(set(ent.text for ent in doc.ents))

def extract_entities(text: str) -> list[str]:
    doc = nlp(text)
    # 只保留有明确意义的实体类型（根据需求调整）
    valid_entity_labels = {
        "PERSON",    # 人名
        "ORG",       # 组织
        "GPE",       # 地理实体（国家、城市等）
        "DATE",      # 日期
        "EVENT",     # 事件
        "WORK_OF_ART"# 作品名
    }
    entities = []
    for ent in doc.ents:
        # 过滤无效实体：只保留指定类型、长度适中、不含换行符的实体
        if (ent.label_ in valid_entity_labels 
            and len(ent.text) <= 100  # 过滤过长文本
            and "\n" not in ent.text):  # 过滤含换行符的文本
            entities.append(ent.text)
    return list(set(entities))  # 去重

def load_entity_cache() -> dict[str, str]:
    if CACHE_PATH.exists():
        return json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    return {}

def save_entity_cache(entity_map: dict[str, str]) -> None:
    CACHE_PATH.write_text(json.dumps(entity_map, ensure_ascii=False, indent=2), encoding="utf-8")

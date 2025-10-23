# src/pipeline.py


import os  # 新增：用于设置环境变量
from prefect import flow, task
from src.chunker import chunk_text
from src.entity_cache import extract_entities, load_entity_cache, save_entity_cache
from src.translate import babel_translate
os.environ["PREFECT_API_URL"] = "http://127.0.0.1:4200/api"

@task
def chunk_step(text: str):
    return chunk_text(text)


@task
def extract_step(chunks: list[str]):
    entities = set()
    for c in chunks:
        entities.update(extract_entities(c))
    return list(entities)


@task
def update_cache_step(entities: list[str]):
    cache = load_entity_cache()
    for e in entities:
        if e not in cache:
            cache[e] = babel_translate(e, source_lang="en", target_lang="zh")
    save_entity_cache(cache)
    return cache


@task
def translate_step(chunk: str, entity_map: dict[str, str]):
    for src, tgt in entity_map.items():
        chunk = chunk.replace(src, f"<ENT:{src}>")
    translated = babel_translate(chunk, source_lang="en", target_lang="zh")
    for src, tgt in entity_map.items():
        translated = translated.replace(f"<ENT:{src}>", tgt)
    return translated



@flow(name="EnglishToChinese_ConsistentTranslation")
def translation_pipeline(text: str) -> str:
    # 关键：在 flow 运行前强制设置 API 地址（适配 3.4.24 版本）
    
    # 1. 分块
    print("📝 正在分块...")
    chunks = chunk_step(text)
    print(f"✅ 文本已分为 {len(chunks)} 个块")
    
    # 2. 提取实体
    print("🔍 正在提取实体...")
    entity_list = extract_step(chunks)
    print(f"✅ 找到 {len(entity_list)} 个实体")
    
    # 3. 更新缓存
    print("💾 正在更新实体缓存...")
    entity_map = update_cache_step(entity_list)
    print(f"✅ 缓存已更新，包含 {len(entity_map)} 个实体翻译")
    
    # 4. 翻译每个块
    print("🌐 正在翻译文本块...")
    translated_chunks = []
    for i, chunk in enumerate(chunks, 1):
        print(f"   翻译块 {i}/{len(chunks)}...")
        translated = translate_step(chunk, entity_map)
        translated_chunks.append(translated)
    
    # 5. 合并结果
    result = "\n\n".join(translated_chunks)
    print("✅ 翻译完成！")
    return result



# from prefect import flow, task
# from src.chunker import chunk_text
# from src.entity_cache import extract_entities, load_entity_cache, save_entity_cache
# from src.translate import babel_translate


# @task
# def chunk_step(text: str):
#     return chunk_text(text)


# @task
# def extract_step(chunks: list[str]):
#     entities = set()
#     for c in chunks:
#         entities.update(extract_entities(c))
#     return list(entities)


# @task
# def update_cache_step(entities: list[str]):
#     cache = load_entity_cache()
#     for e in entities:
#         if e not in cache:
#             cache[e] = babel_translate(e, source_lang="en", target_lang="zh")
#     save_entity_cache(cache)
#     return cache


# @task
# def translate_step(chunk: str, entity_map: dict[str, str]):
#     for src, tgt in entity_map.items():
#         chunk = chunk.replace(src, f"<ENT:{src}>")
#     translated = babel_translate(chunk, source_lang="en", target_lang="zh")
#     for src, tgt in entity_map.items():
#         translated = translated.replace(f"<ENT:{src}>", tgt)
#     return translated


# @flow(name="EnglishToChinese_ConsistentTranslation")
# def translation_pipeline(text: str) -> str:
#     chunks = chunk_step(text)
#     entity_list = extract_step(chunks)
#     entity_map = update_cache_step(entity_list)
#     translated_futures = [translate_step.submit(c, entity_map) for c in chunks]
#     translated_chunks = [f.result() for f in translated_futures]
#     return "\n\n".join(translated_chunks)








# src/pipeline.py

# from prefect import flow, task
# from prefect.settings import PREFECT_API_URL
# from src.chunker import chunk_text
# from src.entity_cache import extract_entities, load_entity_cache, save_entity_cache
# from src.translate import babel_translate

# @task
# def chunk_step(text: str):
#     return chunk_text(text)

# @task
# def extract_step(chunks: list[str]):
#     entities = set()
#     for c in chunks:
#         entities.update(extract_entities(c))
#     return list(entities)

# @task
# def update_cache_step(entities: list[str]):
#     cache = load_entity_cache()
#     for e in entities:
#         if e not in cache:
#             # 翻译实体为中文
#             cache[e] = babel_translate(e, source_lang="en", target_lang="zh")
#     save_entity_cache(cache)
#     return cache

# @task
# def translate_step(chunk: str, entity_map: dict[str, str]):
#     # 替换实体为标记
#     for src, tgt in entity_map.items():
#         chunk = chunk.replace(src, f"<ENT:{src}>")
#     # 调用真实翻译
#     translated = babel_translate(chunk, source_lang="en", target_lang="zh")
#     # 恢复实体翻译
#     for src, tgt in entity_map.items():
#         translated = translated.replace(f"<ENT:{src}>", tgt)
#     return translated

# @flow(name="EnglishToChinese_ConsistentTranslation")
# def translation_pipeline(text: str) -> str:
#     chunks = chunk_step(text)
#     entity_list = extract_step(chunks)
#     entity_map = update_cache_step(entity_list)
#     # 并行翻译每一个 chunk
#     translated_futures = [translate_step.submit(c, entity_map) for c in chunks]
#     translated_chunks = [f.result() for f in translated_futures]
#     result = "\n\n".join(translated_chunks)
#     return result

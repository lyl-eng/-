# src/chunker.py

def chunk_text(text: str, max_len: int = 800) -> list[str]:
    """将长英文文本分段，避免模型上下文超限。"""
    chunks = []
    current = []
    current_len = 0
    for line in text.split('\n'):
        line_len = len(line)
        if current_len + line_len < max_len:
            current.append(line)
            current_len += line_len
        else:
            chunks.append('\n'.join(current))
            current = [line]
            current_len = line_len
    if current:
        chunks.append('\n'.join(current))
    return chunks


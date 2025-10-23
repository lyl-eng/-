# main.py

from pathlib import Path
from src.pipeline import translation_pipeline
# from src.simple_pipeline import translation_pipeline

def main():
    text_path = Path("data/sample.txt")
    text = text_path.read_text(encoding="utf-8")

    translated = translation_pipeline(text)
    output_path = Path("data/translated.txt")
    output_path.write_text(translated, encoding="utf-8")
    print(f"✅ 翻译完成，结果已保存至 {output_path}")

if __name__ == "__main__":
    main()

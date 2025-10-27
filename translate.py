
import os
from babeldoc.translator.translator import OpenAITranslator  # 导入原类

# 继承原类，重写 prompt 方法
class CustomOpenAITranslator(OpenAITranslator):
    def prompt(self, text):
        # 自定义 Prompt：在默认指令基础上，新增“保留标题”的要求
        return [
            {
                "role": "system",
                "content": "You are a professional,authentic machine translation engine. Please keep the title (usually the first line of the text) separate from the body content.",  # 新增标题处理提示
            },
            {
                "role": "user",
                "content": f";; Treat next line as plain text input and translate it into {self.lang_out}. Follow these rules: 1. If the first line is a title, translate it separately and keep it at the top (leave a blank line between title and body). 2. Output translation ONLY, no explanations or notes. 3. If translation is unnecessary (e.g. proper nouns, codes), return the original text. Input:\n\n{text}",  # 明确标题处理规则
            },
        ]

# 修改 babel_translate 函数，使用自定义的翻译器
def babel_translate(text: str, source_lang="en", target_lang="zh") -> str:
    openai_api_key = "..."
    if not openai_api_key:
        raise ValueError("请配置有效的 OpenAI API 密钥")

    # 初始化 自定义翻译器（替换原 OpenAITranslator）
    translator = CustomOpenAITranslator(
        lang_in=source_lang,
        lang_out=target_lang,
        model="gpt-3.5-turbo",
        api_key=openai_api_key,
        base_url="https://api.openai.com/v1",
        ignore_cache=False
    )

    try:
        return translator.translate(text)
    except Exception as e:
        raise RuntimeError(f"OpenAI 翻译失败：{str(e)}")

# 测试代码
if __name__ == "__main__":
    # 临时设置 API 密钥（仅测试用，正式环境建议用环境变量）
    # os.environ["OPENAI_API_KEY"] = "你的实际API密钥"
    
    try:
        result = babel_translate("Hello, world! This is a test translation.")
        print("翻译结果：", result)
    except Exception as e:
        print("错误：", e)

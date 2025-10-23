import os
from babeldoc.translator.translator import OpenAITranslator  # 从你提供的文件导入

def babel_translate(text: str, source_lang="en", target_lang="zh") -> str:
    """使用 BabelDOC 的 OpenAITranslator 进行翻译"""
    # 从环境变量获取 OpenAI API 密钥（推荐），或直接填写（不推荐）
    openai_api_key = "..."
    if not openai_api_key or openai_api_key == "你的API密钥":
        raise ValueError("请配置有效的 OpenAI API 密钥（通过环境变量 OPENAI_API_KEY 或直接填写）")

    # 初始化 OpenAI 翻译器（参数对应代码中的 __init__ 方法）
    translator = OpenAITranslator(
        lang_in=source_lang,         # 源语言（如英文 "en"）
        lang_out=target_lang,        # 目标语言（如中文 "zh"）
        model="gpt-3.5-turbo",       # 模型名称（免费额度可用 gpt-3.5-turbo）
        api_key=openai_api_key,      # 你的 OpenAI API 密钥
        base_url="https://api.openai.com/v1",  # OpenAI 官方接口地址（国内用户可能需要代理）
        ignore_cache=False           # 是否忽略缓存（False 可加速重复翻译）
        
    )

    try:
        # 调用翻译方法（内部会处理缓存、速率限制和重试）
        return translator.translate(text)
    except Exception as e:
        raise RuntimeError(f"OpenAI 翻译失败：{str(e)}")








# import os
# import requests
# from babeldoc.translator.translator import OpenAITranslator

# def babel_translate(text: str, source_lang="en", target_lang="zh") -> str:
#     openai_api_key = "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"
    
#     # 设置代理（Clash默认端口通常是7890）
#     proxy_url = "http://127.0.0.1:7890"
    
#     # 创建带代理的会话
#     session = requests.Session()
#     session.proxies = {
#         "http": proxy_url,
#         "https": proxy_url
#     }
    
#     translator = OpenAITranslator(
#         lang_in=source_lang,
#         lang_out=target_lang,
#         model="gpt-3.5-turbo",
#         api_key=openai_api_key,
#         base_url="https://api.openai.com/v1",
#         ignore_cache=False
#     )
    
#     # 如果OpenAITranslator支持自定义会话，传入session
#     # 如果不支持，可能需要修改babeldoc源码或使用其他方法
    
#     try:
#         return translator.translate(text)
#     except Exception as e:
#         raise RuntimeError(f"OpenAI 翻译失败：{str(e)}")
    





# 测试代码
if __name__ == "__main__":
    # 临时设置 API 密钥（仅测试用，正式环境建议用环境变量）
    # os.environ["OPENAI_API_KEY"] = "你的实际API密钥"
    
    try:
        result = babel_translate("Hello, world! This is a test translation.")
        print("翻译结果：", result)
    except Exception as e:
        print("错误：", e)
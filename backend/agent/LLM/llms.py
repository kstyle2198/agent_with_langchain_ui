from functools import lru_cache
from langchain.chat_models import init_chat_model


@lru_cache(maxsize=1)
def get_qwen3_32b():
    return init_chat_model(
        model="qwen/qwen3-32b",
        model_provider="groq",
        temperature=0,
        max_tokens=3000,
    )

@lru_cache(maxsize=1)
def get_llama_70b():
    return init_chat_model(
        model="llama-3.3-70b-versatile",
        model_provider="groq",
        temperature=0,
        max_tokens=3000,
    )

@lru_cache(maxsize=1)
def get_gptoss_120b():
    return init_chat_model(
        model="openai/gpt-oss-120b",
        model_provider="groq",
        temperature=0,
        max_tokens=3000,
    )

# 사용
QWEN3_32B = get_qwen3_32b()
LLAMA_70B = get_llama_70b()
GPT_OSS_120B = get_gptoss_120b()
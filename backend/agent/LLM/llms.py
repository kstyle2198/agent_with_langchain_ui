from langchain.chat_models import init_chat_model

GPT_OSS_120B = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0,
    max_tokens=3000,
)

LLAMA_70B = init_chat_model(
    model="llama-3.3-70b-versatile",
    model_provider="groq",
    temperature=0,
    max_tokens=3000,
)

QWEN3_32B = init_chat_model(
    model="qwen/qwen3-32b",
    model_provider="groq",
    temperature=0,
    max_tokens=3000,
)
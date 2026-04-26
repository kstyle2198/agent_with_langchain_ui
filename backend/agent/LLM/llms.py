from langchain.chat_models import init_chat_model

GPT_OSS_120B = init_chat_model(
    model="openai/gpt-oss-120b",
    model_provider="groq",
    temperature=0,
    max_tokens=3000,
)
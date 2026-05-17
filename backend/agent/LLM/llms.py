from langchain.chat_models import init_chat_model
from threading import Lock

class QwenModelSingleton:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_model(cls):
        # Double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = init_chat_model(
                        model="qwen/qwen3-32b",
                        model_provider="groq",
                        temperature=0,
                        max_tokens=3000,
                    )
        return cls._instance
    
class LlamaModelSingleton:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_model(cls):
        # Double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = init_chat_model(
                        model="llama-3.3-70b-versatile",
                        model_provider="groq",
                        temperature=0,
                        max_tokens=3000,
                    )
        return cls._instance
    
class GPTOSSModelSingleton:
    _instance = None
    _lock = Lock()

    @classmethod
    def get_model(cls):
        # Double-checked locking
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = init_chat_model(
                        model="openai/gpt-oss-120b",
                        model_provider="groq",
                        temperature=0,
                        max_tokens=3000,
                    )
        return cls._instance


# 사용 예시
QWEN3_32B = QwenModelSingleton.get_model()
LLAMA_70B = LlamaModelSingleton.get_model()
GPT_OSS_120B = GPTOSSModelSingleton.get_model()
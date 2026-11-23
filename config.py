import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv(override=True)

        # APPLICATION
        self.APP_NAME = os.getenv("APP_NAME", "DocuMind")
        self.APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
        self.APP_PORT = int(os.getenv("APP_PORT", "8000"))

        # PROVIDER ENDPOINTS
        self.OLLAMA_HOST = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        ).rstrip("/")

        self.LM_STUDIO_HOST = os.getenv(
            "LM_STUDIO_HOST",
            "http://127.0.0.1:1234/v1"
        ).rstrip("/")

        self.OPENAI_HOST = os.getenv(
            "OPENAI_HOST",
            "https://api.openai.com/v1"
        ).rstrip("/")

        # CHAT MODEL
        self.PROVIDER = os.getenv(
            "PROVIDER",
            "ollama"
        ).strip().lower()

        chat_urls = {
            "ollama": f"{self.OLLAMA_HOST}/v1",
            "lmstudio": self.LM_STUDIO_HOST,
            "cloud": self.OPENAI_HOST
        }

        chat_keys = {
            "ollama": "ollama",
            "lmstudio": "lm-studio",
            "cloud": ""
        }

        chat_models = {
            "ollama": "qwen3:1.7b",
            "lmstudio": "your-loaded-model",
            "cloud": "gpt-4.1-mini"
        }

        if self.PROVIDER not in chat_urls:
            raise ValueError(
                "Invalid PROVIDER. Choose ollama, lmstudio or cloud."
            )

        self.LLM_BASE_URL = chat_urls[self.PROVIDER]

        api_key = os.getenv("API_KEY", "").strip()

        self.API_KEY = api_key or chat_keys[self.PROVIDER]

        self.MODEL = os.getenv(
            "MODEL",
            chat_models[self.PROVIDER]
        )

        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.2"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

        # SYSTEM MESSAGE
        self.SYSTEM_MESSAGE = os.getenv(
            "SYSTEM_MESSAGE",
            "You are DocuMind, an assistant for technical documentation. "
            "Answer using only the provided document context. "
            "If the answer cannot be found, explicitly say so. "
            "Never invent technical specifications or facts."
        )

        # EMBEDDING MODEL
        self.EMBEDDING_PROVIDER = os.getenv(
            "EMBEDDING_PROVIDER",
            self.PROVIDER
        ).strip().lower()

        embedding_urls = {
            "ollama": self.OLLAMA_HOST,
            "lmstudio": self.LM_STUDIO_HOST,
            "cloud": self.OPENAI_HOST
        }

        embedding_keys = {
            "ollama": "ollama",
            "lmstudio": "lm-studio",
            "cloud": ""
        }

        if self.EMBEDDING_PROVIDER not in embedding_urls:
            raise ValueError(
                "Invalid EMBEDDING_PROVIDER. "
                "Choose ollama, lmstudio or cloud."
            )

        self.EMBEDDING_BASE_URL = embedding_urls[
            self.EMBEDDING_PROVIDER
        ]

        embedding_api_key = os.getenv(
            "EMBEDDING_API_KEY",
            ""
        ).strip()

        self.EMBEDDING_API_KEY = (
            embedding_api_key
            or chat_keys[self.PROVIDER]
            if False else
            embedding_api_key
        )

        if not self.EMBEDDING_API_KEY:
            self.EMBEDDING_API_KEY = (
                api_key
                or embedding_keys[self.EMBEDDING_PROVIDER]
            )

        self.EMBEDDING_MODEL = os.getenv(
            "EMBEDDING_MODEL",
            "embeddinggemma:300m"
        )

        # RAG SETTINGS
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
        self.RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "5"))

        # DOCUMENT STORAGE
        self.DOCUMENTS_DIRECTORY = Path(
            os.getenv("DOCUMENTS_DIRECTORY", "./data/documents")
        )

        self.CHROMA_DIRECTORY = Path(
            os.getenv("CHROMA_DIRECTORY", "./data/chroma")
        )

        # Create required directories if they don't exist
        self.DOCUMENTS_DIRECTORY.mkdir(parents=True, exist_ok=True)
        self.CHROMA_DIRECTORY.mkdir(parents=True, exist_ok=True)

        # LOGGING
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
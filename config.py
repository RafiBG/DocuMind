import os
from dotenv import load_dotenv


class Config:
    def __init__(self) -> None:
        load_dotenv()

        # Application
        self.APP_NAME = os.getenv("APP_NAME", "DocuMind")
        self.APP_HOST = os.getenv("APP_HOST", "127.0.0.1")
        self.APP_PORT = int(os.getenv("APP_PORT", "8000"))

        # LLM
        self.PROVIDER = os.getenv("PROVIDER", "ollama")
        self.LLM_BASE_URL = os.getenv(
            "LLM_BASE_URL",
            "http://localhost:11434/v1"
        )
        self.API_KEY = os.getenv("API_KEY", "ollama")
        self.MODEL = os.getenv("MODEL", "qwen3:1.7b")
        self.TEMPERATURE = float(os.getenv("TEMPERATURE", "0.7"))
        self.MAX_TOKENS = int(os.getenv("MAX_TOKENS", "4096"))

        # Embeddings
        self.OLLAMA_HOST = os.getenv(
            "OLLAMA_HOST",
            "http://localhost:11434"
        )
        self.EMBEDDING_MODEL = os.getenv(
            "EMBEDDING_MODEL",
            "embeddinggemma:300m"
        )

        # RAG
        self.CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "800"))
        self.CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "120"))
        self.RETRIEVER_TOP_K = int(os.getenv("RETRIEVER_TOP_K", "5"))

        # Directories
        self.DOCUMENTS_DIRECTORY = os.getenv(
            "DOCUMENTS_DIRECTORY",
            "./data/documents"
        )
        self.CHROMA_DIRECTORY = os.getenv(
            "CHROMA_DIRECTORY",
            "./data/chroma"
        )

        # Logging
        self.LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
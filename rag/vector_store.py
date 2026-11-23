from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_openai import OpenAIEmbeddings
from config import Config


class VectorStoreService:
    def __init__(self, config: Config):
        self.config = config

        self.embeddings = self._create_embeddings()

        self.vector_store = Chroma(
            collection_name="documind_documents",
            embedding_function=self.embeddings,
            persist_directory=config.CHROMA_DIRECTORY
        )

    
    def _create_embeddings(self):
        provider = self.config.EMBEDDING_PROVIDER

        if provider == "ollama":
            return OllamaEmbeddings(
                model=self.config.EMBEDDING_MODEL,
                base_url=self.config.EMBEDDING_BASE_URL
            )

        if provider in ("lmstudio", "cloud"):
            return OpenAIEmbeddings(
                model=self.config.EMBEDDING_MODEL,
                base_url=self.config.EMBEDDING_BASE_URL,
                api_key=self.config.EMBEDDING_API_KEY,
                check_embedding_ctx_length=False
            )

        raise ValueError(
            f"Unsupported embedding provider: {provider}"
        )


    def add_documents(self, documents):
        if not documents:
            return 0

        sources = {
            document.metadata["source"]
            for document in documents
        }

        for source in sources:
            self.vector_store.delete(
                where={"source": source}
            )

        self.vector_store.add_documents(documents)

        return len(documents)

    def search(self, query: str, k: int = 5):
        return self.vector_store.similarity_search(
            query,
            k=k
        )

    def delete_document(self, source: str):
        self.vector_store.delete(
            where={"source": source}
        )

import uvicorn
import webbrowser
import sys
from threading import Timer
from web.app import app
from config import Config
from services.llm_service import LLMService
from services.conversation_memory import ConversationMemoryService
from rag.vector_store import VectorStoreService


def open_browser():
    try:
        print("Opening dashboard...")
        webbrowser.open("http://127.0.0.1:8000")
    except Exception as e:
        print(f"Browser error: {e}")


def main():
    try:
        config = Config()

        # Initialize services
        llm_service = LLMService(config)
        vector_store = VectorStoreService(config)
        conversation_memory = ConversationMemoryService(max_turns=5)

        # Attach services to application state
        app.state.config = config
        app.state.llm_service = llm_service
        app.state.vector_store = vector_store
        app.state.conversation_memory = conversation_memory

        browser_timer = Timer(1.5, open_browser)
        browser_timer.daemon = True
        browser_timer.start()

        print("\n--- Starting DocuMind ---")

        print("Chat provider:", config.PROVIDER)
        print("Chat model:", config.MODEL)

        print("Embedding provider:", config.EMBEDDING_PROVIDER)
        print("Embedding model:", config.EMBEDDING_MODEL)
        print("Embedding URL:", config.EMBEDDING_BASE_URL)

        print("Conversation memory: Enabled")
        print("Memory turns: 5")

        server_config = uvicorn.Config(
            app,
            host=config.APP_HOST,
            port=config.APP_PORT,
            log_level="info"
        )

        server = uvicorn.Server(server_config)
        server.run()

    except KeyboardInterrupt:
        print("\nStopping DocuMind...")

    except Exception as e:
        print(f"Critical Startup Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

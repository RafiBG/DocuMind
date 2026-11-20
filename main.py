import uvicorn
import webbrowser
import sys
from threading import Timer

from web.app import app
from config import Config


def open_browser():
    try:
        print("Opening dashboard...")
        webbrowser.open("http://127.0.0.1:8000")
    except Exception as e:
        print(f"Browser error: {e}")


def main():
    try:
        config = Config()

        # Attach configuration to the application
        app.state.config = config

        # Open browser after server startup
        browser_timer = Timer(1.5, open_browser)
        browser_timer.daemon = True
        browser_timer.start()

        print("\n--- Starting DocuMind ---")

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

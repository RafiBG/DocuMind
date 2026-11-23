from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from config import Config
from api import chat, documents, settings


config = Config()

app = FastAPI(
    title=config.APP_NAME,
    description="Intelligent assistant for technical documentation using LLM and RAG.",
    version="0.1.0"
)

# Allow frontend requests to communicate with the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register API routes
app.include_router(chat.router, prefix="/api/chat", tags=["Chat"])
app.include_router(documents.router, prefix="/api/documents", tags=["Documents"])
app.include_router(settings.router, prefix="/api/settings", tags=["Settings"])


# Frontend directory
WEB_DIRECTORY = Path(__file__).resolve().parent


# Serve CSS and JavaScript files
app.mount(
    "/static",
    StaticFiles(directory=WEB_DIRECTORY),
    name="static"
)


# Serve the main page
@app.get("/")
async def root():
    return FileResponse(WEB_DIRECTORY / "index.html")


@app.get("/health")
async def health():
    return {"status": "healthy"}

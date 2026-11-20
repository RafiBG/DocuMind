from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from api import chat, documents, settings


config = Config()

app = FastAPI(
    title=config.APP_NAME,
    description="Intelligent assistant for technical documentation using LLM and RAG.",
    version="0.1.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register API routes
app.include_router(
    chat.router,
    prefix="/api/chat",
    tags=["Chat"]
)

app.include_router(
    documents.router,
    prefix="/api/documents",
    tags=["Documents"]
)

app.include_router(
    settings.router,
    prefix="/api/settings",
    tags=["Settings"]
)


@app.get("/")
async def root():
    return {
        "application": config.APP_NAME,
        "status": "running",
        "version": "0.1.0"
    }


@app.get("/health")
async def health():
    return {"status": "healthy"}

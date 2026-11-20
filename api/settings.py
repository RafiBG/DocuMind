from fastapi import APIRouter
from config import Config

router = APIRouter()
config = Config()


@router.get("/")
async def get_settings():
    return {
        "application": config.APP_NAME,
        "provider": config.PROVIDER,
        "model": config.MODEL,
        "embedding_model": config.EMBEDDING_MODEL
    }
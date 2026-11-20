from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class ChatRequest(BaseModel):
    question: str


@router.post("/")
async def send_message(request: ChatRequest):
    return {
        "question": request.question,
        "answer": "RAG functionality will be implemented soon.",
        "sources": []
    }
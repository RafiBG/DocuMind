from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_documents():
    return {
        "documents": [],
        "message": "Document management is not implemented yet."
    }
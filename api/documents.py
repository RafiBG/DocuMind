from pathlib import Path
from fastapi import APIRouter, File, HTTPException, Request, UploadFile
from ingestion.pipeline import ingest_pdf

router = APIRouter()


@router.post("/upload")
async def upload_document(
    request: Request,
    file: UploadFile = File(...)
):
    config = request.app.state.config
    vector_store = request.app.state.vector_store

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Missing filename."
        )

    filename = Path(file.filename).name

    if not filename.lower().endswith(".pdf"):
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=400,
            detail="Empty file."
        )

    if len(content) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail="File exceeds the 20 MB limit."
        )

    file_path = Path(config.DOCUMENTS_DIRECTORY) / filename
    file_path.parent.mkdir(parents=True, exist_ok=True)

    file_path.write_bytes(content)

    try:
        chunks = ingest_pdf(
            str(file_path),
            config.CHUNK_SIZE,
            config.CHUNK_OVERLAP
        )

        stored_chunks = vector_store.add_documents(chunks)

        return {
            "filename": filename,
            "pages": len({
                chunk.metadata["page"]
                for chunk in chunks
            }),
            "chunks": stored_chunks,
            "status": "success"
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Document processing failed: {str(e)}"
        )


@router.get("/")
async def list_documents():
    return {
        "documents": [],
        "message": "Document listing will be implemented later."
    }

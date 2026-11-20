
from pathlib import Path
from langchain_core.documents import Document

from ingestion.pdf_loader import load_pdf
from ingestion.text_splitter import split_documents


def ingest_pdf(
    file_path: str,
    chunk_size: int,
    chunk_overlap: int
) -> list[Document]:

    # Extract text from PDF
    documents = load_pdf(file_path)

    # Split extracted text into chunks
    chunks = split_documents(
        documents,
        chunk_size,
        chunk_overlap
    )

    print(f"Processed: {Path(file_path).name}")
    print(f"Extracted pages: {len(documents)}")
    print(f"Generated chunks: {len(chunks)}")

    return chunks

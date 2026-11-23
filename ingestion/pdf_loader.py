import pymupdf
from pathlib import Path
from langchain_core.documents import Document


def load_pdf(file_path: str) -> list[Document]:
    pdf_path = Path(file_path)

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {file_path}")

    documents = []

    with pymupdf.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text").strip()

            if text:
                documents.append(
                    Document(
                        page_content=text,
                        metadata={
                            "source": pdf_path.name,
                            "page": page_number
                        }
                    )
                )

    if not documents:
        raise ValueError(
            "No readable text found in the PDF. "
            "It may be a scanned document."
        )

    return documents

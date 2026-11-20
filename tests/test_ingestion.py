
from langchain_core.documents import Document

from ingestion.text_splitter import split_documents


def test_split_documents():
    text = "Technical documentation example. " * 100

    documents = [
        Document(
            page_content=text,
            metadata={
                "source": "test.pdf",
                "page": 1
            }
        )
    ]

    chunks = split_documents(
        documents,
        chunk_size=200,
        chunk_overlap=30
    )

    assert len(chunks) > 1
    assert chunks[0].metadata["source"] == "test.pdf"
    assert chunks[0].metadata["page"] == 1
    assert chunks[0].metadata["chunk_id"] == 0
    assert all(chunk.page_content for chunk in chunks)

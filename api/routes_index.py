from fastapi import APIRouter, UploadFile, Form
from chunker.chunker import split_text_to_chunks
from chunker.embedder import embed_chunks
from qdrant.indexer import upsert_chunks
from qdrant.schema import create_collection
import fitz
import os

router = APIRouter()

# PDF text extraction
def extract_text(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

@router.post("/add-document")
async def add_document(file: UploadFile, doc_id: str = Form(...)):
    temp_path = f"temp_{file.filename}"

    # save temp file
    with open(temp_path, "wb") as f:
        f.write(await file.read())

    try:
        text = extract_text(temp_path)
        chunks = split_text_to_chunks(text)
        embeddings = embed_chunks(chunks)

        create_collection()
        upsert_chunks(chunks, embeddings, doc_id)

        return {
            "doc_id": doc_id,
            "chunks": len(chunks),
        }
    finally:
        os.remove(temp_path)

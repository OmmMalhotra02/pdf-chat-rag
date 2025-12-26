from fastapi import FastAPI, File, UploadFile # type: ignore
import os
import shutil
from services.pdf_loader import extract_pdf_text
from services.chunker import chunk_pages
from services.embeddings import chunks_to_embeddings

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello world"}

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/uploadFile/')
async def upload_pdf(pdf: UploadFile = File(...)):

    dest_path = os.path.join(UPLOAD_DIR, pdf.filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

    extracted_content_pagewise = extract_pdf_text(dest_path)
    chunks = chunk_pages(extracted_content_pagewise)

    embeddings: list[dict[int, list]] = []

    for chunk in chunks:
        vector = chunks_to_embeddings(chunk["text"])
        # print(embedding)
        embeddings.append({
            "chunk_id": chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "embedding": vector
        })

    return {
            "filename": pdf.filename,
            "message": "PDF uploaded and processed successfully",
            "pages": len(extracted_content_pagewise),
            "chunks": chunks,
            "embeedings": embeddings
        }


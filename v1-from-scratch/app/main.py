from fastapi import FastAPI, File, UploadFile # type: ignore
import os
import shutil
from services.pdf_loader import extract_pdf_text
from services.chunker import chunk_pages
from services.embeddings import chunks_to_embeddings
from services.vector_store import VectorStore
from schemas.schemas import ChatRequest
from services.qa import generate_answer

vector_store = None

app = FastAPI()

@app.get('/')
async def root():
    return {"message": "Hello world"}

UPLOAD_DIR = "data/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/uploadFile/')
async def upload_pdf(pdf: UploadFile = File(...)):
    global vector_store

    dest_path = os.path.join(UPLOAD_DIR, pdf.filename)

    with open(dest_path, "wb") as buffer:
        shutil.copyfileobj(pdf.file, buffer)

    extracted_content_pagewise = extract_pdf_text(dest_path)
    chunks = chunk_pages(extracted_content_pagewise)

    embeddings = []
    metadatas = []

    for chunk in chunks:
        vector = chunks_to_embeddings(chunk["text"])
        embeddings.append(vector)
        metadatas.append({
            "chunk_id": chunk["chunk_id"],
            "page_number": chunk["page_number"],
            "text": chunk["text"]
        })

    vector_store = VectorStore(dim=len(embeddings[0]))
    vector_store.add_embeddings(embeddings, metadatas)

    return {"message": "PDF indexed successfully"}

@app.post("/chat")
async def chat(req: ChatRequest):
    query_vector = chunks_to_embeddings(req.question)
    relevant_chunks = vector_store.search(query_vector, k=5)

    answer = generate_answer(question=req.question, chunks=relevant_chunks)

    return {
        "question": req.question,
        "answer": answer,
        "sources": [
            c["page_number"] for c in relevant_chunks
        ]
    }
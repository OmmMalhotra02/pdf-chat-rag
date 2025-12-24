from fastapi import FastAPI, File, UploadFile # type: ignore
import os
import shutil
from services.pdf_loader import extract_pdf_text
from services.chunker import chunk_pages

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

    return {
            "filename": pdf.filename,
            "message": "PDF uploaded and processed successfully",
            "pages": len(extracted_content_pagewise),
            "chunks": chunks
        }


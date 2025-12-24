from fastapi import FastAPI, File, UploadFile # type: ignore
import os
import shutil

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

    return {
            "filename": pdf.filename,
            "content_type": pdf.content_type,
            "message": "File saved successfully",
            "destination path": dest_path
        }
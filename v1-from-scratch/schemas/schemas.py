from pydantic import BaseModel # type: ignore
from typing import List

class UploadResponse(BaseModel):
    document_id: str
    message: str

class ChatRequest(BaseModel):
    question: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[int]
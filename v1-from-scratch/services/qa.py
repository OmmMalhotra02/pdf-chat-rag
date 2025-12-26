# type: ignore
from google import genai
from dotenv import load_dotenv 
import os

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

client = genai.Client(api_key = api_key)

def generate_answer(question: str, chunks: list[dict]) -> str:

    context_text = "\n\n".join(
        f"(Page {c['page_number']}) {c['text']}"
        for c in chunks
    )

    prompt = f"""
        You are a helpful answering assistant. Use the provided context and our knowledge to give answers.
        If the answer is not present in the context, answer it open endedly after stating:
        "I cannot find this information in the document."

        Context:
        {context_text}

        Question:
        {question}
    """

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents = prompt
    )

    return response.text
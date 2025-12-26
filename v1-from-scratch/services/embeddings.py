from google import genai
import os
from dotenv import load_dotenv # type: ignore

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

def chunks_to_embeddings(text: str) -> list[float]:
    client = genai.Client(api_key=api_key)

    result = client.models.embed_content(
        model="gemini-embedding-001",
        contents=text
    )

    return result.embeddings[0].values
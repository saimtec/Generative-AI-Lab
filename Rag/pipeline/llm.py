import os

from langchain_google_genai import ChatGoogleGenerativeAI

from .config import GEMINI_MODEL, GOOGLE_API_KEY


def create_gemini_llm():
    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is missing. Add it to the project .env file.")

    return ChatGoogleGenerativeAI(
        model=GEMINI_MODEL,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.1,
    )

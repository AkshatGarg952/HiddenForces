import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()


def _build_llm():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise RuntimeError("GOOGLE_API_KEY is not configured for AI battle solving")

    return ChatGoogleGenerativeAI(
        model=os.getenv("AI_BATTLE_MODEL", "gemini-2.5-flash-lite"),
        google_api_key=api_key
    )


def generate_candidate(prompt: str) -> str:
    llm = _build_llm()
    response = llm.invoke(prompt)
    return getattr(response, "content", "") or ""

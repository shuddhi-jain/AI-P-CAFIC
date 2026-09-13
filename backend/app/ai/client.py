from google import genai

from app.config import settings

gemini_client = genai.Client(
    api_key=settings.gemini_api_key
)
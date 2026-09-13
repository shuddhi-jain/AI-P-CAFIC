from fastapi import APIRouter

from app.ai.gemini import test_gemini

router = APIRouter(
    prefix="/ai",\
    tags=["AI"]

)

@router.get("/test")
def test_gemini_endpoint():
    return{
        "response": test_gemini()
    }
from pydantic import BaseModel


class ExtractionResult(BaseModel):
    text: str
    confidence: float | None = None
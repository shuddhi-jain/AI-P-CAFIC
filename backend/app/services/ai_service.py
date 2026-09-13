import base64

from app.ai.client import gemini_client
from app.ai.prompts import SYSTEM_PROMPT, ANALYSIS_PROMPT
from app.schema.ai import ClaimAnalysisResponse

def analyze_document(
        file_content: bytes,
    mime_type: str) -> ClaimAnalysisResponse:

    encoded_file = base64.b64encode(file_content).decode("utf-8")

    response = gemini_client.interactions.create(
        model="gemini-3.8-flash",
        stream=False,
        input=[
            {
                "type": "document",
                "data": encoded_file,
                "mime_type": mime_type,
            },
            {
                            "type": "text",
                            "text": f"{SYSTEM_PROMPT}\n\n{ANALYSIS_PROMPT}",
            },
        ],
          response_format={
            "type": "text",
            "mime_type": "application/json",
            "schema": ClaimAnalysisResponse.model_json_schema(),},
    )

    output_text = getattr(response, "output_text", None)
    if not isinstance(output_text, str):
        raise ValueError("The AI response did not contain text output")

    return ClaimAnalysisResponse.model_validate_json(
        output_text
    )
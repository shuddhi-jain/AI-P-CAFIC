import base64

from google import genai

from app.config import settings

SYSTEM_PROMPT = settings.system_prompt

client = genai.Client(
    api_key=settings.gemini_api_key
)


def analyze_claim(file_path: str):
    uploaded_file = client.files.upload(file=file_path)

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        config={"system_instruction": SYSTEM_PROMPT},
        contents=[
            uploaded_file,
            """
            Analyze this insurance claim document.

            Identify:
            1. Document type
            2. Claim-related information
            3. Important extracted details
            4. Missing information or documents
            5. Potential compliance concerns
            """,
        ],
    )

    return response.text


def analyze_claim_pdf(fileContent: bytes):
    interaction = client.interactions.create(
        model="gemini-3.8-flash",
        input=[
            {
                "type": "document",
                "data": base64.b64encode(fileContent).decode("utf-8"),
                "mime_type": "application/pdf",
            },
            {
                "type": "text",
                "text": f"{SYSTEM_PROMPT}\n\nAnalyze this insurance claim document and provide the required findings.",
            },
        ],
    )

    print(interaction.output_text)

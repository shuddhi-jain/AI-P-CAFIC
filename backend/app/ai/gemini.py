from google import genai

from app.config import settings

client = genai.Client(
    api_key=settings.gemini_api_key
)

def analyze_claim(file_path: str):
    uploaded_file = client.files.upload(
        file=file_path
    )

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents=[
            uploaded_file,
            """
            Analyze this in insurance claim document.

            Identify:
            1. Document type
            2. Claim-related information
            3. Important extracted details
            4. Misisng information or documents
            5. Potential compliance concerns

            Do not invent information.
            Only use inofrmation present in the document


"""
        ]
    )

    return response.text
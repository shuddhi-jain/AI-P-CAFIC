from app.storage.s3 import download_file_from_s3
from app.documents.extractor import extract_text_from_pdf, extract_text_from_image

documents = [
    {
        "name": "PDF",
        "object_key": "claims/1/documents/77f2d8b3-2185-4fcd-8cb4-acb8ca1f3049.pdf",
        "mime_type": "application/pdf"
    },
    {
         "name": "PNG",
          "object_key": "claims/1/documents/ffb67ac4-19c7-4b58-8038-29ec5403726f.png",
          "mime_type": "image/png"
    },
]

for document in documents:
    print(f"\n======= {document['name']} ========")

    file_content = download_file_from_s3(
        document["object_key"]
    )

    print(f"Downloaded: {len(file_content)} bytes")

    if document["mime_type"] == "application/pdf":
        text = extract_text_from_pdf(file_content)

    elif document["mime_type"].startswith("image/"):
        text = extract_text_from_image(file_content)

    else:
        raise ValueError(
            f"Unsupported file type: {document['mime_type']}"
        )

    print(f"Extracted characters: {len(text)}")
    print("\n--- EXTRACTED TEXT ---\n")
    print(text)
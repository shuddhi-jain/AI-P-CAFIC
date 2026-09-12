import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.claim import Claim
from app.models.claim_document import ClaimDocument, DocumentType
from app.models.policy import Policy
from app.models.user import User
from app.schema.claim_document_schema import ClaimDocumentResponse
from app.storage.s3 import upload_file_to_s3, generate_presigned_url


router = APIRouter(
    prefix="/claims",
    tags=["Claim Documents"],
)


@router.post("/{claim_id}/documents", response_model=ClaimDocumentResponse)
def upload_claim_document(
    claim_id: int,
    document_type: DocumentType = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    claim = (
        db.query(Claim)
        .join(Policy, Claim.policy_id == Policy.id)
        .filter(Claim.id == claim_id, Policy.user_id == current_user.id)
        .first()
    )

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found",
        )

    extension = ""
    if file.filename and "." in file.filename:
        extension = "." + file.filename.rsplit(".", 1)[1]

    object_key = f"claims/{claim_id}/documents/{uuid.uuid4()}{extension}"

    file.file.seek(0, 2)
    file_size = file.file.tell()
    file.file.seek(0)

    upload_file_to_s3(
        file.file,
        object_key,
        file.content_type or "application/octet-stream",
    )

    document = ClaimDocument(
        claim_id=claim_id,
        document_type=document_type,
        file_name=file.filename or "unknown",
        file_type=file.content_type or "application/octet-stream",
        file_size=file_size,
        file_url=object_key,
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document


@router.get("/{document_id}/url")
def get_document_url(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    document = (
        db.query(ClaimDocument)
        .join(Claim, Claim.id == ClaimDocument.claim_id)
        .join(Policy, Claim.policy_id == Policy.id)
        .filter(ClaimDocument.id == document_id, Policy.user_id == current_user.id)
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found",
        )

    url = generate_presigned_url(document.file_url)
    return {
        "document_id": document.id,
        "url": url,
        "expires_in": 900,
    }


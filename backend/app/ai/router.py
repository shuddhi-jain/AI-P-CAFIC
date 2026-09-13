from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.claim import Claim
from app.models.claim_document import ClaimDocument
from app.models.policy import Policy
from app.models.user import User
from app.schema.ai import ClaimAnalysisResponse
from app.services.ai_service import analyze_document
from app.storage.s3 import download_file_from_s3

router = APIRouter(
    prefix="/ai",\
    tags=["AI ANALYSIS"]

)

@router.post(
    "/{claim_id}/documents/{document_id}/analyze",
    response_model=ClaimAnalysisResponse
)
def analyzwe_claim_document(
       claim_id: int,
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    document = (
        db.query(ClaimDocument)
        .join(Claim, ClaimDocument.claim_id == Claim.id)
        .join(Policy, Claim.policy_id == Policy.id)
        .filter(
            ClaimDocument.id == document_id,
            ClaimDocument.claim_id == claim_id,
            Policy.user_id == current_user.id
        )
        .first()
    )

    if not document:
        raise HTTPException(
            status_code=404,
            detail="Document not found"
        )

    file_content = download_file_from_s3(
        document.file_url
    )

    result = analyze_document(
        file_content=file_content,
        mime_type=document.file_type
    )

    return result

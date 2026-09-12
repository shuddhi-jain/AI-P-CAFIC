
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models.user import User
from app.schema.claim_schema import ClaimCreate, ClaimResponse
from app.models.claim import Claim
from app.models.policy import Policy


router = APIRouter(
    prefix= "/claims",
    tags=["Claims"]
)

@router.post("/", response_model=ClaimResponse)
def create_claim(
    claim: ClaimCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    policy = db.query(Policy).filter(
        Policy.id == claim.policy_id,
        Policy.user_id == current_user.id).first()

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )
    
    new_claim = Claim(
        policy_id=claim.policy_id,
        claim_number=claim.claim_number,
        claim_amount=claim.claim_amount,
        description=claim.description
    )
    db.add(new_claim)
    db.commit()
    db.refresh(new_claim)
    return new_claim

@router.get("/", response_model=list[ClaimResponse])
def get_claims(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claims = db.query(Claim).join(Policy).filter(
        Policy.user_id == current_user.id
    ).all()

    return claims

@router.get("/{claim_id}", response_model=ClaimResponse)
def get_claim(
    claim_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    claim = db.query(Claim).join(Policy).filter(
        Claim.id == claim_id,
        Policy.user_id == current_user.id
    ).first()

    if not claim:
        raise HTTPException(
            status_code=404,
            detail="Claim not found"
        )

    return claim

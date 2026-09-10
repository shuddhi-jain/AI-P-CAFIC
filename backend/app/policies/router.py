
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.auth.dependencies import get_current_user
from app.database import SessionLocal, get_db
from app.models.user import User
from app.schema.user import UserLogin
from app.auth.securirty import verify_password
from app.schema.policy_schema import PolicyCreate, PolicyResponse
from app.models.policy import Policy


router = APIRouter(
    prefix= "/policy",
    tags=["Policies"]
)

@router.post("/",response_model=PolicyResponse)
def create_policy(policy: PolicyCreate, db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    new_policy = Policy(
        user_id=current_user.id,
        policy_number=policy.policy_number,
        policy_type=policy.policy_type,
        insurer_name=policy.insurer_name,
        insurer_id=policy.insurer_id,
        start_date=policy.start_date,
        end_date=policy.end_date,
        coverage_amount=policy.coverage_amount,
        policy_document_url=policy.policy_document_url
    )
    db.add(new_policy)
    db.commit()
    db.refresh(new_policy)
    return new_policy

@router.get("/",response_model=list[PolicyResponse])
def get_policies(
    db: Session =Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    policies = db.query(Policy).filter(
       Policy.user_id == current_user.id
    ).all()

    return policies

@router.get("/{policy_id}", response_model=PolicyResponse)
def get_policy(
    policy_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    policy = db.query(Policy).filter(
        Policy.id == policy_id,
        Policy.user_id == current_user.id
    ).first()

    if not policy:
        raise HTTPException(
            status_code=404,
            detail="Policy not found"
        )

    return policy

from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.claim import ClaimStatus


class ClaimCreate(BaseModel):
    policy_id: int
    claim_number: str
    claim_amount: float
    description: str


class ClaimResponse(BaseModel):

    id: int
    policy_id: int
    claim_number: str
    claim_amount: float
    claim_date: datetime
    description: str
    status: ClaimStatus
    created_at: datetime

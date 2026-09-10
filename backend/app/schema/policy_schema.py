from pydantic import BaseModel
from datetime import  datetime

class PolicyCreate(BaseModel):
    policy_number: str
    policy_type: str
    insurer_name: str
    insurer_id: str
    start_date: str
    end_date: str
    coverage_amount: float
    status: str
    policy_document_url: str

class PolicyResponse(BaseModel):
    id: int
    user_id: int
    policy_number: str
    policy_type: str
    insurer_name: str
    insurer_id: str
    start_date: datetime
    end_date: datetime
    coverage_amount: float
    policy_document_url: str
    status: str
    created_at: datetime


from pydantic import BaseModel

class PolicyCreate(BaseModel):
    user_id: int
    policy_no: str
    policy_type: str
    insurer_name: str
    insurer_id: str
    start_date: str
    end_date: str
    coverage_amount: float
    policy_document_url: str

class PolicyResponse(BaseModel):
    id: int
    user_id: int
    policy_no: str
    policy_type: str
    insurer_name: str
    insurer_id: str
    start_date: str
    end_date: str
    coverage_amount: float
    policy_document_url: str


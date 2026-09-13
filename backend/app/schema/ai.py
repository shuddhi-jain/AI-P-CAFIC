from typing import Optional

from pydantic import BaseModel


class ComplianceIssue(BaseModel):
    issue: str
    severity: str
    explanation: str


class ClaimInformation(BaseModel):
    patient_name: Optional[str] = None
    claim_number: Optional[str] = None
    hospital_name: Optional[str] = None
    claim_amount: Optional[float] = None
    treatment_date: Optional[str] = None


class ClaimAnalysisResponse(BaseModel):
    document_type: str
    claim_information: ClaimInformation
    missing_information: list[str]
    compliance_issues: list[ComplianceIssue]
    overall_assessment: str
    confidence: float
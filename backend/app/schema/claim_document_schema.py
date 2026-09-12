from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.models.claim_document import DocumentType, ProcessingStatus


class ClaimDocumentCreate(BaseModel):
    claim_id: int
    document_type: DocumentType

class ClaimDocumentResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    claim_id: int
    document_type: DocumentType
    file_name: str
    file_type: str
    file_size: int
    file_url: str
    uploaded_at: datetime
    processing_status: ProcessingStatus

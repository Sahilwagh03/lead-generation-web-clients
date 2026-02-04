from pydantic import BaseModel
from app.constants.batch_status import LeadStatus


class UpdateLeadStatusRequest(BaseModel):
    status: LeadStatus


class LeadStatusResponse(BaseModel):
    id: int
    batch_id: int
    status: LeadStatus

    class Config:
        from_attributes = True  # for SQLAlchemy v2

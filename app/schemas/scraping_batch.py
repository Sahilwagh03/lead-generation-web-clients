from pydantic import BaseModel, Field
from app.constants.batch_status import BatchStatus

class ScrapingBatchCreate(BaseModel):
    hashtag: str = Field(..., min_length=1, max_length=100)
    lead_count: int = Field(..., gt=0)

class ScrapingBatchResponse(BaseModel):
    id: int
    user_id: int
    hashtag: str
    lead_count: int
    status: BatchStatus

    class Config:
        from_attributes = True

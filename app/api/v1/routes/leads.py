from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services.scrape import scrape
router = APIRouter()

# Request body model
class HashtagRequest(BaseModel):
    hashtags: List[str]

@router.post("/generate-leads")
def generate_leads(request: HashtagRequest):
    if not request.hashtags:
        raise HTTPException(status_code=400, detail="Hashtags list cannot be empty")

    try:
        leads = scrape(request.hashtags)
        return {"status": "success", "leads_count": len(leads), "leads": leads}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

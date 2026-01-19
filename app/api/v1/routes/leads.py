import logging
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
from app.services.scrape import scrape
from app.utils.processing.lead_processing import process_leads
from app.db.leads_repo import save_leads
from app.controllers.leads import get_all_leads
logger = logging.getLogger(__name__)


router = APIRouter()
class HashtagRequest(BaseModel):
    hashtags: List[str]
    max_profiles: int = 10
class LeadsRequest(BaseModel):
    leads: List[Dict[str, Any]]

@router.post("/generate-leads")
def generate_leads(request: HashtagRequest):
    if not request.hashtags:
        raise HTTPException(status_code=400, detail="Hashtags list cannot be empty")

    try:
        leads = scrape(request.hashtags, request.max_profiles)
        if leads:
            save_leads(leads)
            return {"status": "success", "leads_count": len(leads)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.post("/process-leads")
async def api_process_leads(request: LeadsRequest):
    try:
        # Empty check
        if not request.leads:
            raise HTTPException(
                status_code=400,
                detail="Leads list cannot be empty"
            )

        result = await process_leads(request.leads)

        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to process leads"
            )

        return {
            "status": "success",
            "processed_count": len(result),
            "leads": result
        }

    except HTTPException:
        # Re-raise FastAPI exceptions
        raise

    except ValueError as e:
        logger.error(f"Value error while processing leads: {e}")
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        logger.exception("Unexpected error while processing leads")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/get-leads")
def fetch_leads(limit: int = 50, offset: int = 0):
    try:
        return {
            "leads": get_all_leads(limit=limit, offset=offset)
        }
    except HTTPException:
        # re-raise FastAPI exceptions safely
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
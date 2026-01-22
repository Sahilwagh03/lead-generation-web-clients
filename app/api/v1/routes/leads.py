import logging
from fastapi import APIRouter, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from app.services.lead_queue import enqueue_scrape_job
from app.utils.processing.lead_processing import process_leads
from app.controllers.leads import get_all_leads , DateFilter
from datetime import date
from app.services.scrape import run_scrape_job
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
        raise HTTPException(
            status_code=400,
            detail="Hashtags list cannot be empty"
        )

    enqueue_scrape_job(request.hashtags, request.max_profiles)

    return {
        "status": "accepted",
        "message": "Lead generation job queued",
        "hashtags": request.hashtags
    }

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
def fetch_leads(
    limit: int = Query(50, ge=1, le=100, description="Number of records to return"),
    offset: int = Query(0, ge=0, description="Number of records to skip"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    is_business: Optional[bool] = Query(None, description="Filter by business type"),
    date_filter: Optional[DateFilter] = Query(None, description="Preset date filter"),
    start_date: Optional[date] = Query(None, description="Custom start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Custom end date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, min_length=1, max_length=100, description="Search term")
):
    """
    Fetch leads with multiple filtering options.
    
    Example queries:
    - /get-leads?date_filter=today
    - /get-leads?start_date=2024-01-01&end_date=2024-01-31
    - /get-leads?is_verified=true&date_filter=this_week
    - /get-leads?search=john&is_business=true
    """
    try:
        leads = get_all_leads(
            limit=limit,
            offset=offset,
            is_verified=is_verified,
            is_business=is_business,
            date_filter=date_filter.value if date_filter else None,
            start_date=start_date,
            end_date=end_date,
            search=search
        )
        
        return {
            "leads": leads,
            "count": len(leads),
            "limit": limit,
            "offset": offset,
            "filters": {
                "is_verified": is_verified,
                "is_business": is_business,
                "date_filter": date_filter,
                "start_date": start_date,
                "end_date": end_date,
                "search": search
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        # Log the actual error for debugging
        print(f"Error fetching leads: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )
from datetime import date
from typing import Optional
from unittest.mock import patch
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.constants.batch_status import BatchStatus
from app.controllers.leads import DateFilter, get_all_leads
from app.core.deps import get_current_user
from app.crud.leads import bulk_update_leads, update_lead_status
from app.db.database import get_db
from app.db.models.users import User
from app.schemas.lead import LeadStatusResponse, UpdateLeadStatusRequest
from app.schemas.scraping_batch import (
    ScrapingBatchCreate,
    ScrapingBatchResponse,
)
from app.crud.scraping_batch import create_scraping_batch, get_batches, update_batch_status
from app.services.lead_queue import enqueue_scrape_job
from app.utils.processing.lead_processing import process_leads

router = APIRouter()

@router.post(
    "/create-scraping-batch",
    response_model=ScrapingBatchResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_scraping_batch_api(
    payload: ScrapingBatchCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    batch = create_scraping_batch(
        db=db,
        hashtag=payload.hashtag,
        lead_count=payload.lead_count,
        user_id=current_user.id,
    )

    # enqueue should NOT break API
    try:
        enqueue_scrape_job(batch.hashtag, batch.lead_count, batch.id ,current_user.id)
    except Exception as e:
        print("Queue error:", e)

    return batch

    
@router.post("/process-leads")
async def api_process_leads(batch_id: int, db: Session = Depends(get_db)):
    try:
        if not batch_id:
            raise HTTPException(
                status_code=400,
                detail="Batch ID cannot be empty"
            )

        result = await process_leads(db,batch_id)

        if result is None:
            raise HTTPException(
                status_code=500,
                detail="Failed to process leads"
            )

        bulk_update_leads(db, result["processed_leads"])
        update_batch_status(db, batch_id, BatchStatus.PROCESSED.value, total_leads=result["total"])

        return {
            "status": "success",
            "processed_count": len(result["processed_leads"]),
            "stats": result["stats"],
        }

    except HTTPException:
        # Re-raise FastAPI exceptions
        raise

    except ValueError as e:
        raise HTTPException(
            status_code=422,
            detail=str(e)
        )

    except Exception as e:
        print(f"Error processing leads: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )


@router.get("/get-leads")
def fetch_leads(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(20, ge=1, le=100, description="Records per page"),
    batch_id: Optional[int] = Query(None, description="Filter by batch id"),
    is_verified: Optional[bool] = Query(None, description="Filter by verification status"),
    is_business: Optional[bool] = Query(None, description="Filter by business type"),
    date_filter: Optional[DateFilter] = Query(None, description="Preset date filter"),
    start_date: Optional[date] = Query(None, description="Custom start date (YYYY-MM-DD)"),
    end_date: Optional[date] = Query(None, description="Custom end date (YYYY-MM-DD)"),
    search: Optional[str] = Query(None, min_length=1, max_length=100, description="Search term"),
    db: Session = Depends(get_db),
):
    """
    Fetch leads with filters + pagination

    Examples:
    - /get-leads?page=1&page_size=20
    - /get-leads?page=2&is_verified=true
    - /get-leads?page=1&search=john
    """
    try:
        offset = (page - 1) * page_size

        leads, total = get_all_leads(
            db=db,
            limit=page_size,
            offset=offset,
            batch_id=batch_id,
            is_verified=is_verified,
            is_business=is_business,
            date_filter=date_filter.value if date_filter else None,
            start_date=start_date,
            end_date=end_date,
            search=search,
            return_total=True
        )

        total_pages = (total + page_size - 1) // page_size if total is not None else 0

        return {
            "leads": leads,
            "pagination": {
                "page": page,
                "page_size": page_size,
                "total": total,
                "total_pages": total_pages,
                "has_next": page < total_pages,
                "has_prev": page > 1,
            },
            "filters": {
                "is_verified": is_verified,
                "is_business": is_business,
                "date_filter": date_filter,
                "start_date": start_date,
                "end_date": end_date,
                "search": search,
            },
        }

    except HTTPException:
        raise
    except Exception as e:
        print(f"Error fetching leads: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")
    
@router.get("/get-batches")
def fetch_batches(db: Session = Depends(get_db),current_user: User = Depends(get_current_user)):
    """
    Fetch all scraping batches from the database.
    """
    try:
        batches = get_batches(db, current_user.id)
        return {
            "status": "success",
            "batches": list(reversed(batches))  # Return in descending order
        }
    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail="Failed to fetch batches"
        )
    
@router.patch("/{lead_id}/status", response_model=LeadStatusResponse)
def update_status(
    lead_id: int,
    payload: UpdateLeadStatusRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return update_lead_status(
        db=db,
        lead_id=lead_id,
        status=payload.status,
        user_id=current_user.id
    )

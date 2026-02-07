from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
import os

from app.db.database import get_db
from app.services.summary_service import generate_all_users_summary

router = APIRouter(prefix="/internal", tags=["Internal"])

CRON_SECRET = os.getenv("CRON_SECRET")


@router.post("/generate-daily-summary")
def generate_summary(
    x_api_key: str = Header(...),
    db: Session = Depends(get_db)
):
    if x_api_key != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    generate_all_users_summary(db)

    return {"message": "Daily summaries generated"}
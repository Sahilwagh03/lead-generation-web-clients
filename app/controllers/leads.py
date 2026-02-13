from datetime import date, timedelta
from typing import Optional, Tuple, List, Dict
from enum import Enum
from fastapi.params import Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
from app.constants.batch_status import LeadStatus
from app.db.database import SessionLocal
from app.db.models.lead import Lead

class DateFilter(str, Enum):
    TODAY = "today"
    TOMORROW = "tomorrow"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this_week"
    THIS_MONTH = "this_month"


def get_date_range(filter_type: str) -> Optional[tuple[date, date]]:
    """
    Returns start_date and end_date for preset filters.
    """
    today = date.today()
    
    filters = {
        "today": (today, today),
        "tomorrow": (today + timedelta(days=1), today + timedelta(days=1)),
        "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
        "this_week": (
            today - timedelta(days=today.weekday()),
            today - timedelta(days=today.weekday()) + timedelta(days=6),
        ),
        "this_month": (
            today.replace(day=1),
            (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1),
        ),
    }
    
    return filters.get(filter_type.lower())


def get_all_leads(
    db: Session,
    user_id: int,
    limit: int = 200,
    offset: int = 0,
    batch_id: Optional[int] = None,
    is_verified: Optional[bool] = None,
    is_business: Optional[bool] = None,
    date_filter: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    status: Optional[LeadStatus] = None,
    return_total: bool = False,
) -> Tuple[List[Dict], Optional[int]]:

    try:
        query = db.query(Lead).filter(Lead.user_id == user_id)
        # ✅ Batch filter
        if batch_id is not None:
            query = query.filter(Lead.batch_id == batch_id)

        if is_verified is not None:
            query = query.filter(Lead.is_verified == is_verified)

        if is_business is not None:
            query = query.filter(Lead.is_business == is_business)

        if status is not None:
            query = query.filter(Lead.status == status)

        if date_filter:
            dr = get_date_range(date_filter)
            if dr:
                query = query.filter(
                    Lead.created_at >= dr[0],
                    Lead.created_at <= dr[1]
                )

        if start_date:
            query = query.filter(Lead.created_at >= start_date)

        if end_date:
            query = query.filter(Lead.created_at <= end_date)

        if search:
            search_term = f"%{search}%"
            query = query.filter(
                or_(
                    Lead.full_name.ilike(search_term),
                    Lead.email.ilike(search_term),
                    Lead.phone.ilike(search_term),
                )
            )

        total = query.order_by(None).count() if return_total else None

        leads = (
            query.order_by(Lead.id.asc())  # stable order
            .limit(limit)
            .offset(offset)
            .all()
        )

        leads_list = [lead.__dict__ for lead in leads]
        for lead in leads_list:
            lead.pop("_sa_instance_state", None)

        return leads_list, total

    finally:
        db.close()
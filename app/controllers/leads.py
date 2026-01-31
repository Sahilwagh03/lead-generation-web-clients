from app.db.database import get_db_connection

from datetime import date, timedelta
from typing import Optional
from enum import Enum

class DateFilter(str, Enum):
    TODAY = "today"
    TOMORROW = "tomorrow"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this_week"
    THIS_MONTH = "this_month"

from app.db.database import get_db_connection
from datetime import date, timedelta
from typing import Optional, Tuple, List, Dict
from enum import Enum

class DateFilter(str, Enum):
    TODAY = "today"
    TOMORROW = "tomorrow"
    YESTERDAY = "yesterday"
    THIS_WEEK = "this_week"
    THIS_MONTH = "this_month"


def get_all_leads(
    limit: int = 50,
    offset: int = 0,
    is_verified: Optional[bool] = None,
    is_business: Optional[bool] = None,
    date_filter: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    return_total: bool = False,   # 👈 NEW
) -> Tuple[List[Dict], Optional[int]]:
    """
    Fetch leads with filtering + pagination.
    Returns (leads, total_count) if return_total=True
    """

    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        base_query = "FROM leads WHERE 1=1"
        params = []

        # Boolean filters
        if is_verified is not None:
            base_query += " AND is_verified = ?"
            params.append(1 if is_verified else 0)

        if is_business is not None:
            base_query += " AND is_business = ?"
            params.append(1 if is_business else 0)

        # Preset date filter
        if date_filter:
            date_range = get_date_range(date_filter)
            if date_range:
                base_query += " AND DATE(created_at) BETWEEN ? AND ?"
                params.extend(date_range)

        # Custom date range
        if start_date:
            base_query += " AND DATE(created_at) >= ?"
            params.append(start_date.isoformat())

        if end_date:
            base_query += " AND DATE(created_at) <= ?"
            params.append(end_date.isoformat())

        # Search
        if search:
            base_query += """
                AND (
                    name LIKE ? OR
                    email LIKE ? OR
                    phone LIKE ?
                )
            """
            search_param = f"%{search}%"
            params.extend([search_param, search_param, search_param])

        # ---- TOTAL COUNT QUERY ----
        total = None
        if return_total:
            count_query = f"SELECT COUNT(*) {base_query}"
            cursor.execute(count_query, params)
            total = cursor.fetchone()[0]

        # ---- DATA QUERY ----
        data_query = f"""
            SELECT *
            {base_query}
            ORDER BY created_at DESC
            LIMIT ? OFFSET ?
        """
        cursor.execute(data_query, params + [limit, offset])
        rows = cursor.fetchall()

        leads = [dict(row) for row in rows]

        return leads, total

    finally:
        conn.close()


def get_date_range(filter_type: str) -> Optional[tuple[str, str]]:
    """
    Get date range based on filter type.
    Returns tuple of (start_date, end_date) in ISO format.
    """
    today = date.today()
    
    filters = {
        "today": (today, today),
        "tomorrow": (today + timedelta(days=1), today + timedelta(days=1)),
        "yesterday": (today - timedelta(days=1), today - timedelta(days=1)),
        "this_week": (
            today - timedelta(days=today.weekday()),
            today - timedelta(days=today.weekday()) + timedelta(days=6)
        ),
        "this_month": (
            today.replace(day=1),
            (today.replace(day=1) + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        ),
    }
    
    date_range = filters.get(filter_type.lower())
    if date_range:
        return (date_range[0].isoformat(), date_range[1].isoformat())
    return None
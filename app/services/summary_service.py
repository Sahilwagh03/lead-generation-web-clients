# =============================================
# app/services/summary_service.py
# FINAL WORKING VERSION (IST SAFE)
# =============================================

from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, time
import pytz

from app.db.models.notifications import Notification
from app.db.models.users import User
from app.db.models.lead import Lead
from app.db.models.scraping_batch import ScrapingBatch
from app.constants.EmailTemplates.summary_template import daily_summary_email_template
from app.services.email_service import send_email


# ======================================================
# TIMEZONE CONFIG (INDIA BUSINESS)
# ======================================================
IST = pytz.timezone("Asia/Kolkata")


# ======================================================
# HELPER → GET YESTERDAY WINDOW (IST → UTC)
# ======================================================
def get_ist_utc_window():
    """
    Example:

    If now = 14 Feb 01:00 IST

    Window should be:
    13 Feb 00:00 IST → 14 Feb 00:00 IST

    Converted to UTC:
    12 Feb 18:30 → 13 Feb 18:30
    """

    now_ist = datetime.now(IST)

    today = now_ist.date()
    yesterday = today - timedelta(days=1)

    start_ist = IST.localize(datetime.combine(yesterday, time.min))
    end_ist = IST.localize(datetime.combine(today, time.min))

    # Convert to UTC for DB filtering
    start_utc = start_ist.astimezone(pytz.utc)
    end_utc = end_ist.astimezone(pytz.utc)

    return start_utc, end_utc


# ======================================================
# MAIN ENTRY
# ======================================================
def generate_all_users_summary(db: Session):
    """Generate daily summary for all users"""

    users = db.query(User).all()

    for user in users:
        try:
            generate_user_summary(db, user)
        except Exception as e:
            print(f"❌ Failed for user {user.id}: {e}")


# ======================================================
# PER USER SUMMARY
# ======================================================
def generate_user_summary(db: Session, user: User):
    """
    Generates yesterday summary using IST calendar
    """

    start, end = get_ist_utc_window()

    print(f"\n📅 IST Window (UTC converted): {start} → {end}")

    # -------------------------------------------------
    # LEAD STATS (FILTER BY USER + WINDOW)
    # -------------------------------------------------
    stats = (
        db.query(Lead.status, func.count(Lead.id))
        .filter(Lead.user_id == user.id)
        .filter(Lead.created_at >= start)
        .filter(Lead.created_at < end)
        .group_by(Lead.status)
        .all()
    )

    print("📊 Lead stats:", stats)

    status_map = {status: count for status, count in stats}

    # -------------------------------------------------
    # SCRAPED COUNT
    # -------------------------------------------------
    scraped = (
        db.query(func.coalesce(func.sum(ScrapingBatch.lead_count), 0))
        .filter(ScrapingBatch.user_id == user.id)
        .filter(ScrapingBatch.created_at >= start)
        .filter(ScrapingBatch.created_at < end)
        .scalar()
    )

    print("📦 Scraped:", scraped)

    # -------------------------------------------------
    # SUMMARY DATA
    # -------------------------------------------------
    summary_data = {
        "new": status_map.get("NEW", 0),          # ⭐ important
        "retarget": status_map.get("RETARGET", 0),
        "contacted": status_map.get("CONTACTED", 0),
        "meetings": status_map.get("MEETING", 0),
        "scraped": scraped or 0,
    }

    message = f"""
Yesterday Summary:

New: {summary_data['new']}
Retarget: {summary_data['retarget']}
Contacted: {summary_data['contacted']}
Meetings: {summary_data['meetings']}
Scraped: {summary_data['scraped']}
""".strip()

    # -------------------------------------------------
    # SAVE NOTIFICATION
    # -------------------------------------------------
    notif = Notification(
        user_id=user.id,
        title="Daily Lead Summary",
        message=message,
        type="SUMMARY",
    )

    db.add(notif)
    db.commit()

    # -------------------------------------------------
    # EMAIL
    # -------------------------------------------------
    subject = "Daily Lead Summary"
    html_message = daily_summary_email_template(summary_data)

    send_email(
        to_email=user.email,
        subject=subject,
        message=message,
        html_message=html_message,
    )

    print(f"✅ Summary sent to {user.email}")

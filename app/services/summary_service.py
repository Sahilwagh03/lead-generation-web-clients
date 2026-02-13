from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta , time
from app.db.models.notifications import Notification
from app.db.models.users import User
from app.db.models.lead import Lead
from app.db.models.scraping_batch import ScrapingBatch
from app.constants.EmailTemplates.summary_template import daily_summary_email_template
from app.services.email_service import send_email


def generate_all_users_summary(db: Session):
    """Generate daily lead summary for all users."""
    users = db.query(User).all()
    
    for user in users:
        generate_user_summary(db, user)


def generate_user_summary(db: Session, user: User):
    """
    Generates yesterday summary (00:00 → 23:59 UTC)
    """

    # -------------------------------------------------
    # FIXED DATE RANGE (full yesterday)
    # -------------------------------------------------
    today = datetime.utcnow().date()
    yesterday = today - timedelta(days=1)

    start = datetime.combine(yesterday, time.min)  # 00:00
    end = datetime.combine(today, time.min)        # next day 00:00

    print(f"\n📅 Summary window: {start} → {end}")

    # -------------------------------------------------
    # Lead status stats
    # -------------------------------------------------
    stats = (
        db.query(Lead.status, func.count(Lead.id))
        .filter(Lead.created_at >= start)
        .filter(Lead.created_at < end)
        .group_by(Lead.status)
        .all()
    )

    print("📊 Lead stats:", stats)

    if not stats:
        print("⚠️ No leads found for this window")
        return

    status_map = {status: count for status, count in stats}

    # -------------------------------------------------
    # Scraped count
    # -------------------------------------------------
    scraped = (
        db.query(func.sum(ScrapingBatch.lead_count))
        .filter(ScrapingBatch.created_at >= start)
        .filter(ScrapingBatch.created_at < end)
        .scalar()
        or 0
    )

    print("📦 Scraped:", scraped)

    # -------------------------------------------------
    # Prepare summary
    # -------------------------------------------------
    summary_data = {
        "retarget": status_map.get("RETARGET", 0),
        "contacted": status_map.get("CONTACTED", 0),
        "meetings": status_map.get("MEETING", 0),
        "scraped": scraped,
    }

    message = f"""
Yesterday Summary:

Retarget: {summary_data['retarget']}
Contacted: {summary_data['contacted']}
Meetings: {summary_data['meetings']}
Scraped: {summary_data['scraped']}
""".strip()

    # -------------------------------------------------
    # Save notification
    # -------------------------------------------------
    notif = Notification(
        user_id=user.id,
        title="Daily Lead Summary",
        message=message,
        type="SUMMARY",
    )

    db.add(notif)
    db.commit()


    # Send summary email
    subject = "Daily Lead Summary"
    html_message = daily_summary_email_template(summary_data)
    send_email(to_email=user.email, subject=subject, message=message, html_message=html_message)

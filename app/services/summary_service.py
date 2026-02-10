from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

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
    """Generate daily lead summary for a single user."""
    yesterday = datetime.utcnow() - timedelta(days=1)

    # Get lead stats for yesterday
    stats = (
        db.query(Lead.status, func.count(Lead.id))
        .filter(Lead.created_at >= yesterday)
        .group_by(Lead.status)
        .all()
    )

    if not stats:
        return  # nothing to summarize

    # Map lead status to count
    status_map = {status: count for status, count in stats}

    # Get total scraped leads yesterday
    scraped = (
        db.query(func.sum(ScrapingBatch.lead_count))
        .filter(ScrapingBatch.created_at >= yesterday)
        .scalar()
        or 0
    )

    # Prepare summary data
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
"""

    # Save notification in DB
    notif = Notification(
        user_id=user.id,
        title="Daily Lead Summary",
        message=message.strip(),
        type="SUMMARY"
    )
    db.add(notif)
    db.commit()

    # Send summary email
    subject = "Daily Lead Summary"
    html_message = daily_summary_email_template(summary_data)
    send_email(to_email=user.email, subject=subject, message=message, html_message=html_message)

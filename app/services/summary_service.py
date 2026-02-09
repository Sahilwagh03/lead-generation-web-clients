from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db.models.notifications import Notification
from app.db.models.users import User
from app.db.models.lead import Lead
from app.db.models.scraping_batch import ScrapingBatch
from app.services.notification_service import send_summary_whatsapp


def generate_all_users_summary(db: Session):
    users = db.query(User).all()

    for user in users:
        generate_user_summary(db, user.id)


def generate_user_summary(db: Session, user):
    yesterday = datetime.utcnow() - timedelta(days=1)

    stats = (
        db.query(Lead.status, func.count(Lead.id))
        .filter(Lead.created_at >= yesterday)
        .group_by(Lead.status)
        .all()
    )

    if not stats:
        return

    status_map = {s: c for s, c in stats}

    scraped = (
        db.query(func.sum(ScrapingBatch.lead_count))
        .filter(ScrapingBatch.created_at >= yesterday)
        .scalar() or 0
    )

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

    notif = Notification(
        user_id=user.id,
        title="Daily Lead Summary",
        message=message.strip(),
        type="SUMMARY"
    )

    db.add(notif)
    db.commit()

    # ⭐ WhatsApp send (legal)
    send_summary_whatsapp(user, summary_data)


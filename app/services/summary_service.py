from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.db.models.notifications import Notification
from app.db.models.users import User
from app.db.models.lead import Lead
from app.db.models.scraping_batch import ScrapingBatch


def generate_all_users_summary(db: Session):
    users = db.query(User).all()

    for user in users:
        generate_user_summary(db, user.id)


def generate_user_summary(db: Session, user_id: int):
    yesterday = datetime.utcnow() - timedelta(days=1)

    stats = (
        db.query(Lead.status, func.count(Lead.id))
        .filter(Lead.created_at >= yesterday)
        .group_by(Lead.status)
        .all()
    )

    status_map = {s: c for s, c in stats}

    scraped = (
        db.query(func.sum(ScrapingBatch.lead_count))
        .filter(ScrapingBatch.created_at >= yesterday)
        .scalar() or 0
    )

    message = f"""
Yesterday Summary:

Retarget: {status_map.get('RETARGET', 0)}
Contacted: {status_map.get('CONTACTED', 0)}
Meetings: {status_map.get('MEETING', 0)}
Scraped: {scraped}
"""

    notif = Notification(
        user_id=user_id,
        title="Daily Lead Summary",
        message=message.strip(),
        type="SUMMARY"
    )

    db.add(notif)
    db.commit()

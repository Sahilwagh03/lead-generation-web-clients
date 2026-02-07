from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models.notifications import Notification
from app.schemas.notifications import NotificationOut

router = APIRouter(prefix="/notifications", tags=["Notifications"])


# -------------------------
# GET unread
# -------------------------
@router.get("/unread", response_model=List[NotificationOut])
def get_unread(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Notification)
        .filter(
            Notification.user_id == user_id,
            Notification.is_read == False
        )
        .order_by(Notification.created_at.desc())
        .all()
    )


# -------------------------
# mark read
# -------------------------
@router.post("/mark-read/{notification_id}")
def mark_read(notification_id: int, db: Session = Depends(get_db)):
    (
        db.query(Notification)
        .filter(Notification.id == notification_id)
        .update({"is_read": True})
    )

    db.commit()

    return {"success": True}

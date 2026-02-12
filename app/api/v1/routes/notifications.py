from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.deps import verify_token
from app.db.database import get_db
from app.db.models.notifications import Notification
from app.schemas.notifications import NotificationOut

router = APIRouter(prefix="/notifications", tags=["Notifications"],dependencies=[Depends(verify_token)])


# -------------------------
# GET all notifications
# -------------------------
@router.get("/", response_model=List[NotificationOut])
def get_all(user_id: int, db: Session = Depends(get_db)):
    return (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .order_by(Notification.created_at.desc())
        .all()
    )

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

# -------------------------
# POST  mark all read
# -------------------------
@router.post("/mark-all-read")
def mark_all_read(user_id: int, db: Session = Depends(get_db)):
    (
        db.query(Notification)
        .filter(Notification.user_id == user_id, Notification.is_read == False)
        .update({"is_read": True})
    )
    db.commit()
    return {"success": True}

@router.delete("/delete-notifications")
def delete_all_notifications(user_id: int, db: Session = Depends(get_db)):
    (
        db.query(Notification)
        .filter(Notification.user_id == user_id)
        .delete()
    )

    db.commit()

    return {"success": True}

from datetime import datetime, timezone
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.db.models.lead import Lead  # We'll create this model

def save_leads(leads: list, batch_id: int):
    """
    Save a list of leads to the database with default values if some fields are missing.
    Associates all leads with the given batch_id.
    """
    session: Session = SessionLocal()
    now = datetime.now(timezone.utc)

    lead_objects = []

    for lead in leads:
        lead_obj = Lead(
            batch_id=batch_id,
            followers=lead.get("followers", 0),
            following=lead.get("following", 0),
            posts=lead.get("posts", 0),
            bio=lead.get("bio", ""),
            website=lead.get("website", ""),
            email=lead.get("email", ""),
            phone=lead.get("phone", ""),
            whatsapp=lead.get("whatsapp", ""),
            is_verified=lead.get("is_verified", False),
            is_business=lead.get("is_business", False),
            category=lead.get("category", ""),
            full_name=lead.get("full_name", ""),
            profile_url=lead.get("profile_url", ""),
            username=lead.get("username", ""),
            created_at=now,
        )
        lead_objects.append(lead_obj)

    try:
        session.add_all(lead_objects)
        session.commit()
        print(f"💾 Saved {len(lead_objects)} leads successfully for batch {batch_id}")
        return True
    except Exception as e:
        session.rollback()
        print(f"❌ Failed to save leads: {e}")
        return False
    finally:
        session.close()

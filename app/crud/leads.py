from typing import List, Dict, Any
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.constants.batch_status import LeadStatus
from app.db.models.lead import Lead


def bulk_update_leads(db: Session, enriched_leads: List[Dict[str, Any]]) -> None:
    """
    Fast + reliable bulk update.

    ✔ single commit
    ✔ skips None
    ✔ auto matches real DB columns
    ✔ works with JSON fields
    """

    if not enriched_leads:
        return

    allowed_columns = {c.name for c in Lead.__table__.columns}

    update_payload = []

    for lead in enriched_leads:
        if not lead.get("id"):
            continue

        row = {"id": lead["id"]}

        for key, value in lead.items():
            if key in allowed_columns and value is not None:
                row[key] = value

        update_payload.append(row)

    if update_payload:
        db.bulk_update_mappings(Lead, update_payload)
        db.flush()
        db.commit()


def update_lead_status(db, lead_id: int, status: str, user_id: int):
    lead = (
        db.query(Lead)
        .filter(
            Lead.id == lead_id,
            Lead.user_id == user_id
        )
        .first()
    )

    if not lead:
        raise HTTPException(404, "Lead not found")

    lead.status = status
    db.commit()
    db.refresh(lead)

    return lead
from sqlalchemy import func
from sqlalchemy.orm import Session
from app.db.models.scraping_batch import ScrapingBatch
from app.schemas.scraping_batch import ScrapingBatchCreate
from app.constants.batch_status import BatchStatus

def create_scraping_batch(
    db: Session,
    batch_in: ScrapingBatchCreate,
) -> ScrapingBatch:
    batch = ScrapingBatch(
        hashtag=batch_in.hashtag,
        lead_count=batch_in.lead_count,
        status=BatchStatus.PENDING.value,
    )
    db.add(batch)
    db.commit()
    db.refresh(batch)
    return batch


def update_batch_status(
    db: Session, batch_id: int, status: str, total_leads: int = 0
) -> None:
    """
    Update the status of a scraping batch.
    status: "pending", "completed", "failed"
    total_leads: number of leads scraped
    """
    batch = db.query(ScrapingBatch).filter(ScrapingBatch.id == batch_id).first()
    if not batch:
        print(f"⚠️ Batch with id={batch_id} not found")
        return

    batch.status = status
    if total_leads:
        batch.total_leads = total_leads
    batch.updated_at = func.now()

    try:
        db.commit()
        print(f"✅ Batch {batch_id} updated to '{status}'")
    except Exception as e:
        db.rollback()
        print(f"❌ Failed to update batch {batch_id}: {e}")

def get_batches(db:Session):
    batches = db.query(ScrapingBatch).all()
    return batches
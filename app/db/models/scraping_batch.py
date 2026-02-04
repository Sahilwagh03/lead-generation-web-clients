from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base

class ScrapingBatch(Base):
    __tablename__ = "scraping_batches"

    id = Column(Integer, primary_key=True, index=True)
    hashtag = Column(String(100), nullable=False)
    lead_count = Column(Integer, default=0)

    status = Column(
        String(20),
        nullable=False,
        default="PENDING",
        index=True,
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

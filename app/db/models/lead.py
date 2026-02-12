from sqlalchemy import Column, Enum, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from app.constants.batch_status import LeadStatus
from app.db.database import Base


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True)
    batch_id = Column(Integer, ForeignKey("scraping_batches.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    posts = Column(Integer, default=0)

    bio = Column(String, default="")
    website = Column(String, default="")
    email = Column(String, default="")
    phone = Column(String, default="")
    whatsapp = Column(String, default="")

    is_verified = Column(Boolean, default=False)
    is_business = Column(Boolean, default=False)

    category = Column(String, default="")
    full_name = Column(String, default="")

    profile_url = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)

    created_at = Column(DateTime)

    # ✅ NEW COLUMNS (IMPORTANT)
    lead_type = Column(String, index=True)
    platform_detected = Column(String)
    pitch_angle = Column(String)

    tags = Column(JSONB)             # list[str]
    website_phones = Column(JSONB)   # list[str]


    status = Column(
        Enum(LeadStatus, name="lead_status_enum"),
        default=LeadStatus.NEW,
        nullable=False,
        index=True,
    )


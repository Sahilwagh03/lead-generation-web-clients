from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool

from app.core.config import DATABASE_URL, ENV


# =========================
# SQLAlchemy Base
# =========================
class Base(DeclarativeBase):
    pass


# =========================
# Engine
# =========================
engine = create_engine(
    DATABASE_URL,

    # pooling
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,

    # production safety
    pool_pre_ping=True,      # reconnect dead connections
    pool_recycle=1800,      # avoid stale connections
)


# =========================
# Session
# =========================
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


# =========================
# Dependency
# =========================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

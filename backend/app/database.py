"""
SkillBridge AI — Database Configuration

Handles SQLAlchemy engine, session, and base model setup.
Uses SQLite as the default database.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import settings

# SQLite requires check_same_thread=False for FastAPI's async nature
connect_args = {}
db_url = settings.database_url
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)

if db_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(db_url, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Base class for all database models."""
    pass


def get_db():
    """
    FastAPI dependency that provides a database session.
    Automatically closes the session after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """
    Create all database tables.
    Called on application startup.
    """
    import app.models
    import app.models.analysis
    Base.metadata.create_all(bind=engine)

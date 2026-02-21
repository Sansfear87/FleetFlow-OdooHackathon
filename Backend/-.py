# database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Import settings from config.py
from core.config import settings


# Create database engine (connection pool)
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=5,        # keep 5 ready connections
    max_overflow=10,    # allow 10 extra connections under load
    pool_pre_ping=True, # check connection health automatically
    echo=False          # set True if you want SQL logs
)


# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all SQLAlchemy models
class Base(DeclarativeBase):
    pass


# FastAPI dependency to get DB session safely
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
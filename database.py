import os, logging
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.pool import QueuePool
load_dotenv()
logger = logging.getLogger(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is not set in .env")
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
engine = create_engine(DATABASE_URL, poolclass=QueuePool, pool_size=5, max_overflow=10,
    pool_timeout=30, pool_recycle=1800, pool_pre_ping=True,
    echo=os.getenv("SQL_ECHO","false").lower()=="true")
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False, expire_on_commit=False)
class Base(DeclarativeBase): pass
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
def verify_database_connection():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        logger.info("Database connected.")
    except Exception as exc:
        raise RuntimeError(f"DB connection failed: {exc}") from exc

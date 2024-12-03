from core.config import get_settings
from sqlalchemy.orm import sessionmaker,declarative_base
from sqlalchemy import create_engine
from typing import Generator

settings = get_settings()
print(settings.DATABASE_URL)
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=300,
    pool_size=5,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    
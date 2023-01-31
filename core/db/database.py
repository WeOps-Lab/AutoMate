from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.settings import settings

engine = create_engine(settings.db_url, echo=True, pool_recycle=3600, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


def get_db():
    try:
        db = Session()
        yield db
    finally:
        db.close()


def get_session():
    return Session()

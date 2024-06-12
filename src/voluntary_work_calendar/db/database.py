from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from voluntary_work_calendar.config import Config


# SQLALCHEMY_DATABASE_URL = "sqlite:///./calendar.db"
SQLALCHEMY_DATABASE_URL = Config.DATABASE_URL_AIVEN

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    # connect_args={"check_same_thread": False}
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

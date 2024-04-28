from voluntary_work_calendar.db.database import Base, SessionLocal, engine
from voluntary_work_calendar.db.models import *


Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        return db
    finally:
        db.close()

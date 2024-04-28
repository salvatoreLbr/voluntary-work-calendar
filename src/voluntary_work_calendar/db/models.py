from sqlalchemy import (
    Column,
    Integer,
    String,
)

from voluntary_work_calendar.db.database import Base


class Calendar(Base):
    __tablename__ = "Calendar"

    id = Column(Integer, primary_key=True)
    data = Column(String(10))
    orario_da = Column(String(5))
    orario_a = Column(String(5))
    name = Column(String(100))


class Users(Base):
    __tablename__ = "Users"

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True)
    role = Column(String(100))
    hashed_password = Column(String)


class Volunteers(Base):
    __tablename__ = "Volunteers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True)

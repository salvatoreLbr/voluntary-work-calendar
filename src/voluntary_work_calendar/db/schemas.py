from typing import Optional
from pydantic import BaseModel


class CalendarBase(BaseModel):
    data: str
    orario_da: str
    orario_a: str
    name: str


class CalendarCreate(CalendarBase):
    pass


class Calendar(CalendarBase):
    id: int
    data: str
    orario_da: str
    orario_a: str
    name: str


class User(BaseModel):
    username: str
    role: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class UserInDBCreate(UserInDB):
    pass


class VolunteersBase(BaseModel):
    data: str
    name: str


class VolunteersCreate(VolunteersBase):
    pass


class Volunteers(VolunteersBase):
    id: int
    name: str

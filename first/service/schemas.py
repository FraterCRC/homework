from datetime import datetime, date
from enum import Enum

from pydantic import BaseModel
class Gender(str, Enum):
    male = 'male'
    female = 'female'


class UserBase(BaseModel):
    id: str
    password: str
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    hobbies: list[str]
    city: str

class UserRegister(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    birth_date: date
    gender: Gender
    hobbies: list[str]
    city: str

class UserLogin(BaseModel):
    username: str
    password: str

# Pydantic models for the request and response bodies of the API

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional

class UserOut(BaseModel): # (user.py) response model for the verify_user and get_user
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True # renamed to from_attributes but causes problems for sqlalchemy

class StudentLogin(BaseModel):
    institution: str
    id: str
    password: str

class Token(BaseModel): # (auth.py) response model for the login and studLogin
    access_token: str
    token_type: str

class TokenData(BaseModel): # (oauth2.py) used to store the user_id for verify_access_token
    id: Optional[str] = None


class ExamCreate(BaseModel): # (exam.py) request model for the create_exam
    #institution: str # taken from the JWT
    name: str
    date: date
    qstn_count: int
    max_marks: int
    
    avg_marks: Optional[int] = None
    contestants: Optional[int] = None
    #mark_each: Optional[list[int]] = None
    #answer_key: Optional[str] = None
    #answers: Optional[list[str]] = None

class ExamOut(BaseModel): # (exam.py) response model for the create_exam and get_exam
    #id: int
    name: str
    #created_at: datetime
    table_name: str

    class Config:
        orm_mode = True    
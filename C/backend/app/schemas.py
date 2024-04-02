# Pydantic models for the request and response bodies of the API

from pydantic import BaseModel, EmailStr
from pydantic.types import conint
from datetime import datetime, date
from typing import Optional

'''
class PostBase(BaseModel):
    title: str
    content: str
    published: bool=True

class PostCreate(PostBase): # owner_id is also needed for the table posts, we will take it from the token 
    pass
'''
'''
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserOut # returns this pydantic model

    class Config:   # to convert to a pydantic model since this class is used as a response
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        orm_mode = True
'''
class UserOtp(BaseModel): # (user.py) request model for the create_otp
    email: EmailStr
    otp: Optional[int] = None
    name: Optional[str] = None
    password: Optional[str] = None

class UserCreate(BaseModel): # (user.py) request model for the verify_user
    email: EmailStr
    otp: int
    password: str
    name: str

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
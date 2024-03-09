# store table models as sqlalchemy models without having to open postgres software

from enum import unique
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class User(Base):
    __tablename__ = "institutions"

    name = Column(String, nullable=False, unique=True) # has to be unique to avoid confusion for students
    email = Column(String, primary_key=True, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    otp = Column(Integer, nullable=True)

    
class Student(Base):
    __tablename__ = "students"

    institution = Column(String, ForeignKey('institutions.name'), nullable=False)
    id = Column(String, nullable=False)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    __table_args__ = (PrimaryKeyConstraint('institution', 'id'),)
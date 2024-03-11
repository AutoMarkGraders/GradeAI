# store table models as sqlalchemy models without having to open postgres software

from enum import unique
from sqlalchemy import Column, Integer, String, ARRAY, Text, ForeignKey, PrimaryKeyConstraint, UniqueConstraint
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


class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, nullable=False)
    institution = Column(String, ForeignKey('institutions.name'), nullable=False)
    name = Column(String, nullable=False)
    max_marks = Column(Integer, nullable=False)
    qstn_count = Column(Integer, nullable=False)
    mark_each = Column(ARRAY(Integer), nullable=True)
    answer_key = Column(Text, nullable=True)
    answers = Column(ARRAY(String), nullable=True)
    contestants = Column(Integer, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    __table_args__ = (UniqueConstraint('institution', 'name'),)


'''
from sqlalchemy import Table, MetaData, Column, Integer, String
from sqlalchemy.sql import text

def create_exam_table(institution: str, name: str, max_marks: int, qstn_count: int):
    metadata = MetaData()

    table_name = f"{institution}_{name}"
    table = Table(
        table_name,
        metadata,
        Column('max_marks', Integer, nullable=False),
        Column('qstn_count', Integer, nullable=False),
        # add other columns as needed
    )

    engine = create_engine('postgresql://user:password@localhost/dbname')
    metadata.create_all(engine)    
'''
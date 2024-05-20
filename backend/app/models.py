# store table models as sqlalchemy models without having to open postgres software

from sqlalchemy import Column, Integer, String, ARRAY, Date, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from .database import Base

class Exam(Base):
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, nullable=False)
    institution = Column(String, nullable=False)
    name = Column(String, nullable=False)
    date = Column(Date, nullable=False)
    qstn_count = Column(Integer, nullable=False)
    max_marks = Column(Integer, nullable=False)
    
    avg_marks = Column(Integer, nullable=True)
    contestants = Column(Integer, nullable=True, default=0)
    #mark_each = Column(ARRAY(Integer), nullable=True)
    #answer_key = Column(Text, nullable=True)
    #answers = Column(ARRAY(String), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)

    __table_args__ = (UniqueConstraint('institution', 'name'),)


class Student(Base):
    __tablename__ = "students"

    email = Column(String, primary_key=True, nullable=False)
    institution = Column(String, nullable=False)
    exams_attended = Column(ARRAY(String), nullable=True)



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
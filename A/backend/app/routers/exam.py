from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, insert

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/exam",
    tags=['Exams'] # for documentation
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ExamOut)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    #print(current_user.name)
    new_exam = models.Exam(institution=current_user.name, **dict(exam))
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)

    # Create a new table for the exam
    metadata = MetaData(bind=db.get_bind())
    table_name = f"{new_exam.institution}_{new_exam.name}"
    columns = [Column('student_id', String, primary_key=True)]
    for i in range(1, new_exam.qstn_count + 1):
        columns.append(Column(f'ans{i}', String))
        columns.append(Column(f'mark{i}', Integer))
    columns.append(Column('total', Integer))    
    table = Table(table_name, metadata, *columns, extend_existing=True)
    metadata.create_all()

    return new_exam


@router.post("/anskey/{tname}", status_code=status.HTTP_201_CREATED)
def upload_anskey(anskey: dict, tname: str, db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user)):
    akey = {"student_id": "answerkey"}
    akey.update(anskey)
    #add total also
    
    # Create a reference to the table
    metadata = MetaData(bind=db.get_bind())
    t = Table(tname, metadata, autoload_with=db.get_bind())

    # Insert akey as a new row into the table
    stmt = insert(t).values(**akey)
    db.execute(stmt)
    db.commit()

    return {"message": f"Answer key inserted into {tname}"}
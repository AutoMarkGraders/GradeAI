#functions to view the exams


from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session, load_only
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, desc, text
from typing import List

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError

router = APIRouter(
    prefix="/view",#starting of all url in this page
    tags=['Views'] # for documentation
)

@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ExamsView])#view/ exam function is hosted here
def view_exams(pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    rows = pdb.query(models.Exam).filter(models.Exam.institution == current_user).all()
    
    # Convert the SQLAlchemy models to Pydantic models to select only the required fields
    exams = [schemas.ExamsView(**row.__dict__) for row in rows]

    return exams


@router.get("/{exam_name}", status_code=status.HTTP_200_OK)#/view/exam_name
def view_exam(exam_name: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    table_name = f"{current_user}_{exam_name}"

    # Reflect the table from the database
    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    table = Table(table_name, metadata, autoload_with=pdb.bind)

    # Query the table based on total
    rows = pdb.execute(table.select().order_by(desc('total'))).fetchall()
    # Convert rows to list of dictionaries
    rows_as_dicts = [row._asdict() for row in rows]
    
    return rows_as_dicts


'''
@router.get("/student", status_code=status.HTTP_200_OK)
def stud_exams(pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    # Reflect the table from the database
    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    table = Table(table_name, metadata, autoload_with=pdb.bind)

    # Query the table based on total
    rows = pdb.execute(table.select().order_by(desc('total'))).fetchall()
    # Convert rows to list of dictionaries
    rows_as_dicts = [row._asdict() for row in rows]
    
    return rows_as_dicts
'''
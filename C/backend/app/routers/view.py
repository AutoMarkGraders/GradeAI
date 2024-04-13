from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session, load_only
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, func, text
from typing import List

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError

router = APIRouter(
    prefix="/view",
    tags=['Views'] # for documentation
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[schemas.ExamsView])
def view_exams(pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    rows = pdb.query(models.Exam).filter(models.Exam.institution == current_user).all()
    
    # Convert the SQLAlchemy models to Pydantic models to select only the required fields
    exams = [schemas.ExamsView(**row.__dict__) for row in rows]

    return exams


@router.get("/{exam_name}", status_code=status.HTTP_200_OK)
def view_exam(exam_name: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):

    table_name = f"{current_user}_{exam_name}"

    # Reflect the table from the database
    metadata = MetaData()
    table = Table(table_name, metadata, autoload_with=pdb.get_bind())

    # Query the table
    query = table.select()
    result = pdb.execute(query)
    rows = result.fetchall()

    # Filter out the answer columns
    filtered_rows = []
    for row in rows:
        row_dict = dict(row)
        filtered_row = {key: value for key, value in row_dict.items() if not key.startswith('ans')}
        filtered_rows.append(filtered_row)

    return filtered_rows

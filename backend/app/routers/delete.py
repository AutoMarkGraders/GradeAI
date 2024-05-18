from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, insert
from sqlalchemy import inspect

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError

router = APIRouter(
    prefix="/delete",
    tags=['delete'] # for documentation
)


@router.delete("/{exam_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exam(exam_name: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    exam = pdb.query(models.Exam).filter(models.Exam.institution == current_user, models.Exam.name == exam_name).first() # changed to first() to get the first exam with the given name and institution
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")#stuff below raise wont run

    #Delete the table with the name current_user_exam_name
    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    table_name = current_user + "_" + exam_name
    table = Table(table_name, metadata, autoload_with=pdb.bind)
    inspector = inspect(pdb.get_bind())
    if inspector.has_table(table_name):
        table.drop(pdb.bind)   

    pdb.delete(exam) #delete the row from the exams table
    pdb.commit()
        
    # DELETE table_name FROM FIREBASE students
    
    return {"detail": "Exam"+ exam_name+"deleted successfully"}

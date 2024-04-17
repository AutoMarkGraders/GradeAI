
#functions to delete data from table

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, func

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError

router = APIRouter(
    prefix="/delete",
    tags=['delete'] # for documentation
)


@router.delete("/{exam_name}", status_code=status.HTTP_204_NO_CONTENT)#delete request
def delete_exam(exam_name: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    
    exam = pdb.query(models.Exam).filter(models.Exam.institution == current_user, models.Exam.name == exam_name).first() # changed to first() to get the first exam with the given name and institution
    if not exam:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exam not found")#stuff below raise wont run

    #else:
    #Delete the table with the name current_user_exam_name
    table_name = current_user + "_" + exam_name
    metadata = MetaData(bind=pdb.get_bind())

    table = Table(table_name, metadata, autoload_with=pdb.bind)
    if table.exists():
        table.drop(pdb.bind)

    pdb.delete(exam)
    pdb.commit()
        

    return {"detail": "Exam"+ exam_name+"deleted successfully"}

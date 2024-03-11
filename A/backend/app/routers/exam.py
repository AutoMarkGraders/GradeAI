from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from .. import schemas, models, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/exam",
    tags=['Exams'] # for documentation
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ExamOut)
def create_exam(exam: schemas.ExamCreate, db: Session = Depends(get_db)):
    new_exam = models.Exam(**dict(exam))
    db.add(new_exam)
    db.commit()
    db.refresh(new_exam)
    return new_exam

#functions to write to table

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, String, MetaData, insert, func

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError
from firebase_admin import storage

router = APIRouter(
    prefix="/exam",
    tags=['Exams'] # for documentation
)

@router.post("/create", status_code=status.HTTP_201_CREATED, response_model=schemas.ExamOut)
def create_exam(exam: schemas.ExamCreate, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    # insert details into the exams table
    new_exam = models.Exam(institution=current_user, **dict(exam))
    pdb.add(new_exam)
    pdb.commit()
    pdb.refresh(new_exam)

    # Create a new table for the exam
    metadata = MetaData(bind=pdb.get_bind())
    table_name = f"{new_exam.institution}_{new_exam.name}"
    columns = [Column('student_id', String, primary_key=True)]
    for i in range(1, new_exam.qstn_count + 1):
        columns.append(Column(f'ans{i}', String))
        columns.append(Column(f'mark{i}', Integer))
    columns.append(Column('total', Integer))
    columns.append(Column('grade', String))    
    table = Table(table_name, metadata, *columns, extend_existing=True)
    metadata.create_all()

    return {"name": new_exam.name, "table_name": table_name}


@router.post("/anskey/{tname}", status_code=status.HTTP_201_CREATED)
def upload_anskey(anskey: dict, tname: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    akey = {"student_id": "answerkey"}
    akey.update(anskey) #adds individual answers and marks to akey
    total = sum(value for i, value in enumerate(anskey.values()) if i % 2 != 0) #total marks
    akey['total'] = total
    
    # Create a reference to the table
    metadata = MetaData(bind=pdb.get_bind())
    t = Table(tname, metadata, autoload_with=pdb.get_bind())

    # Insert akey as a new row into the table
    stmt = insert(t).values(**akey)
    pdb.execute(stmt)
    pdb.commit()

    return {"message": f"Answer key inserted into {tname}"}


@router.post("/anspdf/{tname}", status_code=status.HTTP_201_CREATED)
def upload_pdf(tname: str, student: str = Form(...), file: UploadFile = File(...), pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    # add student if not present in firebase authentication
    student_email = f"{student}@{current_user}.student"
    try:
        user = auth.get_user_by_email(student_email)
    except FirebaseError:
        user = auth.create_user(email=student_email)

    
    db_path = f'students/{current_user}/exams/{tname}'


    # Upload the PDF file to Firebase Storage
    ''' bucket = storage.bucket()
    blob = bucket.blob(file.filename)
    blob.upload_from_file(file.file)
    pdf_url = blob.public_url'''

    # Store metadata in Firebase Realtime Database
    ref = db.reference(db_path)
    new_entry = ref.push({
        'student': student
        #'pdf_url': pdf_url
    })
    return {"message": "PDF uploaded successfully"}


     

    # add tname under student in firebase @BEJ    

    # add pdf to firebase storage @BEJ
















    # ocr pdf and create ans dict @DR

    ans = { #dummy ans dict for testing
    "student_id": f"{student}",
    "ans1": "hello there",
    "ans2": "general kenobi"
    }

    # Grade using Gemini

    # Insert ans as a new row into the table
    metadata = MetaData(bind=pdb.get_bind()) # Create a reference to the tname table
    t = Table(tname, metadata, autoload_with=pdb.get_bind())
    stmt = insert(t).values(**ans)
    pdb.execute(stmt)
    pdb.commit()

    return {"message": f"Answer inserted into {tname}"}
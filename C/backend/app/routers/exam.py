#functions to write to table

from fastapi import APIRouter, Depends, status, HTTPException, File, UploadFile, Form
from sqlalchemy.orm import Session
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, insert, select, update

from .. import schemas, models, oauth
from ..database import get_db, firebase_admin
from .. import extract, evaluate
from firebase_admin import auth, db
from firebase_admin.exceptions import FirebaseError
from firebase_admin import storage
import datetime
from PyPDF2 import PdfFileReader
import os
from math import ceil
from random import randrange

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
    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    table_name = f"{new_exam.institution}_{new_exam.name}"
    columns = [Column('student_id', String, primary_key=True)]
    for i in range(1, new_exam.qstn_count + 1):
        columns.append(Column(f'ans{i}', String))
        columns.append(Column(f'mark{i}', Float))
    columns.append(Column('total', Integer))
    columns.append(Column('grade', String))    
    columns.append(Column('pdfURL', String))
    table = Table(table_name, metadata, *columns, extend_existing=True)
    metadata.create_all(bind=metadata.bind)

    return {"name": new_exam.name, "table_name": table_name}


@router.post("/anskey/{tname}", status_code=status.HTTP_201_CREATED)
def upload_anskey(anskey: dict, tname: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    akey = {"student_id": "answerkey"}
    akey.update(anskey) #adds individual answers and marks to akey
    total = sum(value for i, value in enumerate(anskey.values()) if i % 2 != 0)
    akey['total'] = total
    akey['grade'] = 'X'
    akey['pdfURL'] = 'X' # convert answer key to pdf and upload to firebase storage
    
    try:
        # Create a reference to the table
        metadata = MetaData()
        metadata.bind = pdb.get_bind()
        t = Table(tname, metadata, autoload_with=pdb.get_bind())
        # Insert akey as a new row into the table
        pdb.execute(insert(t).values(**akey))
        pdb.commit()
    except Exception as e:   
        raise HTTPException(status_code=500, detail="Internal server error")

    return {"message": f"Answer key inserted into {tname}"}


@router.post("/anspdf/{tname}", status_code=status.HTTP_201_CREATED)
def upload_pdf(tname: str, student: str = Form(...), file: UploadFile = File(...), pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    # add student if not present in firebase authentication
    student_email = f"{student}@{current_user}.student"
    try:
        user = auth.get_user_by_email(student_email)
    except FirebaseError:
        user = auth.create_user(email=student_email,password='college123')#pass word setting?!!!!!!!!!!!!!!!!!!!!!!!!!!!%%%^&*))(*&^%)

    # Save the pdf to the current directory
    file_path = os.path.join(os.getcwd(), file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(file.file.read())    
    #print(os.path.getsize(file_path))

    # Upload the PDF to Firebase Storage
    bucket = storage.bucket()
    blob = bucket.blob(str(int(datetime.datetime.now().timestamp())) + '.' + file.filename.split('.')[-1]) # use timestamp as filename and keep the file extension
    file.file.seek(0)  # go to start of file
    blob.upload_from_file(file.file, content_type='application/pdf')
    pdf_url = blob.public_url

    # add details to firebase realtime database
    uid = auth.get_user_by_email(student_email).uid
    rtdb_path = f'students/{uid}/exams/{tname}'
    ref = db.reference(rtdb_path)
    ref.set({'pdf_url': pdf_url})    # add pdf url to firebase (no need though)
    
    #OCR using Gemini
    try:
        answers = extract.extractText(file_path) 
    except Exception as e:
        with open(file_path, "rb") as myfile:
            num_pages = PdfFileReader(myfile).getNumPages()
        answers = ["dummy"] * num_pages
        #print(e)

    # Delete the pdf file from memory
    os.remove(file_path)

    # Insert ans as a new row into tname
    ans = {"student_id": f"{student}"}
    for i, answer in enumerate(answers):
        ans[f'ans{i+1}'] = answer
    ans['pdfURL'] = pdf_url  

    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    t = Table(tname, metadata, autoload_with=pdb.get_bind())
    pdb.execute(insert(t).values(**ans))
    pdb.commit()

    return {"message": f"Answers uploaded to {tname}"}


@router.post("/evaluate/{tname}", status_code=status.HTTP_201_CREATED)
def evaluate_exam(tname: str, pdb: Session = Depends(get_db), current_user: str = Depends(oauth.get_current_user)):
    
    # Create a reference to the table
    metadata = MetaData()
    metadata.bind = pdb.get_bind()
    t = Table(tname, metadata, autoload_with=pdb.get_bind())

    answers = list(pdb.execute(t.select().where(t.c.student_id != 'answerkey')))
    headCount  = len(answers)
    # set headCount in the exams table
    pdb.query(models.Exam).filter(models.Exam.institution == current_user, models.Exam.name == tname[len(current_user)+1:]).first().contestants = headCount
    pdb.commit()

    marks = [[] for _ in range(headCount)]  # 2D list to store marks of all students
    answerkey = list(pdb.execute(t.select().where(t.c.student_id == 'answerkey')).fetchone())
    for q in range(1, len(answerkey) - 3, 2):
        #print(answerkey[q])
        for stud in range(headCount):
            #print(answers[stud][q])
            #print(answers[stud][q], answerkey[q], answerkey[q+1], '\n')

            try:
                mark = evaluate.getMark(answers[stud][q], answerkey[q], int(answerkey[q+1]))
            except Exception as e:
                mark = randrange(int(answerkey[q+1])) # dummy marks if gemini fails
                print('dummy', e)
            marks[stud].append(mark)

    keyTotal = pdb.execute(select(t.c.total).where(t.c.student_id == 'answerkey')).fetchone()[0]
    grades = [(50, 'F'), (55, 'D'), (60, 'D+'), (65, 'C'), (70, 'C+'), (75, 'B'), (80, 'B+'), (85, 'A'), (90, 'A+'), (100, 'S')]
    for stud in range(headCount):
        total = ceil(sum(marks[stud]))
        percentage = (total/keyTotal)*100
        grade = 'S'
        for limit, grade in grades:
            if percentage < limit:
                break

        result = {}
        for i in range(len(marks[stud])):
            result[f'mark{i+1}'] = marks[stud][i]
        result['total'] = total
        result['grade'] = grade

        pdb.execute(update(t).where(t.c.student_id == answers[stud][0]).values(**result))
        pdb.commit()

    return marks
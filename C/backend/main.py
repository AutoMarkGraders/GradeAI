import re
from pdfminer.high_level import extract_pages, extract_text

from fastapi import FastAPI, Body, HTTPException, Response, status, Depends, Form, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware

#uvicorn main:app --reload

app = FastAPI()

origins = ["*"] # domains which can talk to api

app.add_middleware( 
    CORSMiddleware, #middleware runs before every request
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




@app.post("/upload")
def uploadPDF(file: UploadFile = File(...)):
    print("hello there")
    if file.filename.endswith('.pdf'):
        text = extract_text(file.filename)
        print(text)
        return {"message": "File uploaded successfully"}
    else:
        return {"error": "Only PDF files are allowed"}


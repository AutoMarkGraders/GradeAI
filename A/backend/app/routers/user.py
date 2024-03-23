from fastapi import HTTPException, status, Depends, APIRouter
from sqlalchemy.orm import Session
import random
from .. import models, schemas, utils
from ..database import get_db

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv 
import os

router = APIRouter(
    prefix="/users",
    tags=['Users']
)

@router.post("/otp", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_otp(user: schemas.UserOtp, db: Session = Depends(get_db)):
    # write code to check if user already exists
    otp = random.randint(1000, 9999)    # generate an otp
    
    # send email
    smtp_object = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    from_address = "notalan.notification@gmail.com"
    to_address = user.email
    load_dotenv()  # Will still attempt to load from .env if it exists
    smtp_object.login(from_address, os.getenv('gmail_api'))
    msg = MIMEMultipart()
    msg['From'] = from_address
    msg['To'] = to_address
    msg['Subject'] = "OTP for GradeAI sign-up"
    #body = 'Greetings from GradeAI,\n\tuse this OTP to complete the registration of your Institution in GradeAI:\n\n\t{}\n\n\n\nIgnore this message if this was not you.'.format(otp)
    html = f"""
        <div style="font-family: Helvetica,Arial,sans-serif;min-width:1000px;overflow:auto;line-height:2">
        <div style="margin:50px auto;width:70%;padding:20px 0">
            <div style="border-bottom:1px solid #eee">
                <a href="" style="font-size:1.4em;color: #00466a;text-decoration:none;font-weight:600">GradeAI</a>
            </div>
            <p style="font-size:1.1em">Greetings,</p>
            <p>Thank you for choosing GradeAI. Use the following OTP to complete your Institution Sign Up.<br>OTP is valid for 5 minutes.</p>
            <h2 style="background: #00466a;margin: 0 auto;width: max-content;padding: 0 10px;color: #fff;border-radius: 4px;">{otp}</h2>
            <p>If this was not you, please ignore.</p>
            <p style="font-size:0.9em;">Regards,<br />GradeAI</p>
            <hr style="border:none;border-top:1px solid #eee" />
            <div style="float:right;padding:8px 0;color:#aaa;font-size:0.8em;line-height:1;font-weight:300">
                <p>GradeAI Inc</p>
                <p>Conspiracy Road</p>
                <p>Pathanamthitta</p>
            </div>
        </div>
        </div>
    """
    msg.attach(MIMEText(html, 'html'))
    smtp_object.sendmail(from_address, to_address, msg.as_string())
    smtp_object.quit()

    user.otp = otp
    user.password = str(otp) # temporary
    user.name = str(otp) # temporary
    temp_user = models.User(**dict(user)) 
    db.add(temp_user)
    db.commit()
    db.refresh(temp_user)
    return temp_user

@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def verify_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    realOTP = db.query(models.User).filter(models.User.email == user.email).first().otp
    if realOTP != user.otp:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="OTP not verified")

    user.otp = None # no longer needed
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**dict(user))
    db.query(models.User).filter(models.User.email == user.email).delete()  # delete the existing row
    db.commit()
    db.add(new_user)    # now the row won't have otp (since otp no longer needed)
    db.commit()
    db.refresh(new_user)
    return new_user

''' without otp verification
@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**dict(user)) 
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
'''

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user with that id not found")
    return user

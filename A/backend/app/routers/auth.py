from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm # used instead of a pydantic model
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=['Authentication'])

@router.post('/login', response_model=schemas.Token)    # POST request due to security reasons
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username).first() # passwordreqform only has username and password

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.name}) # create a token using oauth2.py

    return {"access_token": access_token, "token_type": "bearer"} # how will the front end store this?


@router.post('/login/student', response_model=schemas.Token)
def studLogin(user_credentials: schemas.StudentLogin, db: Session = Depends(database.get_db)):

    # assuming password is not hashed, change later
    user = db.query(models.Student).filter(models.Student.id == user_credentials.id).filter(models.Student.institution == user_credentials.institution).filter(models.Student.password == user_credentials.password).first() 

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    #if not utils.verify(user_credentials.password, user.password):
    #    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id}) # create a token using oauth2.py

    return {"access_token": access_token, "token_type": "bearer"} # how will the front end store this?

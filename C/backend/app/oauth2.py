# JWT expires every 30 mins

from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas, database, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login') # login is the URL that Postman would use to get the token.

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict): # used in routers/auth.py/login and studLogin
    to_encode = data.copy() # {"user_id": 'RSET'} or {"user_id": 'u2103021'}
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})   # {"user_id": 'RSET', "exp": expire-datetime}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# used by below func to verify JWT and retrieve user info
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) # if JWT has expired, decode() will raise an exception
        id: str = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=id)   # simply stores the user_id
    except JWTError:
        raise credentials_exception # JWT expired or invalid
    return token_data

# gets the token from the Authorization header of the HTTP request with Depends(oauth2_scheme)
# how is the front end supposed to pass token as input to this function?
# used in routers to identify the user making the request
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail = "Couldnt validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)   # simply stores the user_id
    # works only for institutions table
    user = db.query(models.User).filter(models.User.name == token.id).first()
    return user

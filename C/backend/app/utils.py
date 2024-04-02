# used in auth and user routers

from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") # settings for password hashing


def hash(password: str):
    return pwd_context.hash(password)   # returns hashed password

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) # returns True or False
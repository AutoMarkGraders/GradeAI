#function to communicate PG Amin and FireBase


from .config import settings # for access to env vars(db config)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from sqlalchemy.ext.declarative import declarative_base     # for creating Base class for making table objects

Base = declarative_base()   # inherited by table objects

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(settings.database_username, settings.database_password, settings.database_hostname, settings.database_port, settings.database_name)
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# dependency function which gets called by routers
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


import os
from dotenv import load_dotenv
import firebase_admin
from firebase_admin import credentials
#from firebase_admin import auth, db

load_dotenv() # Load from .env file
cred = credentials.Certificate(os.getenv('FIREBASE_FILE_PATH'))

# Initialize the Firebase Admin SDK
firebase_admin.initialize_app(cred, {
    'databaseURL' : 'https://auto-mark-grader-default-rtdb.firebaseio.com/'
})

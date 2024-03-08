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


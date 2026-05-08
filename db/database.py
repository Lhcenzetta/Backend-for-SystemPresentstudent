from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

URL_DATABASE =  os.getenv("url")

engine = create_engine(URL_DATABASE)

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from sqlalchemy.orm import Session

# Création dyal l-objets (mn l-image li sifti)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
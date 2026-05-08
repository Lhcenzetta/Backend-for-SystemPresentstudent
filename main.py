from fastapi import FastAPI
from db.database import engine
from db.database import Base

Base.metadata.create_all(engine)

app = FastAPI()
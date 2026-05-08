from fastapi import FastAPI 
from router import api
from db.database import engine
from db.database import Base

Base.metadata.create_all(engine)

app = FastAPI()


app.include_router(api.router)
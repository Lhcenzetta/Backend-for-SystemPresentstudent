from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv
from sqlalchemy.engine import create_engine

load_dotenv()

URL_DATABASE =  f"postgresql+psycopg2://{os.getenv('user')}:{os.getenv('password')}@{os.getenv('host')}:{os.getenv('port')}/{os.getenv('database')}"

engine = create_engine(URL_DATABASE)

Base = declarative_base()
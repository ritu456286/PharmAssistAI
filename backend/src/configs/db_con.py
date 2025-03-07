import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.db.medicine import Base
from langchain_community.utilities import SQLDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_PATH = os.path.join(BASE_DIR, "../db/pharmacy.db")  
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)    

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


db = SQLDatabase.from_uri(DATABASE_URL)

def initialize_db():
    Base.metadata.create_all(bind=engine)   

    
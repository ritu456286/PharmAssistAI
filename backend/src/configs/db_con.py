import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.db.medicine import Base


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_PATH = os.path.join(BASE_DIR, "../db/pharmacy.db")  
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(DATABASE_URL)    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def initialize_db():
    Base.metadata.create_all(bind=engine)   

    
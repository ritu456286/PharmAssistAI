import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.db.database import Base
from langchain_community.utilities import SQLDatabase

BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
DB_DIR = os.path.join(BASE_DIR, "../db")
DB_PATH = os.path.join(BASE_DIR, "../db/pharmacy.db")  
DATABASE_URL = f"sqlite:///{DB_PATH}"


# Ensure the database directory exists
os.makedirs(DB_DIR, exist_ok=True)

engine = create_engine(DATABASE_URL)    

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# LangChain SQLDatabase utility
db = SQLDatabase.from_uri(DATABASE_URL)

def initialize_db():
    """Initialize the database and create all tables."""
    Base.metadata.create_all(bind=engine)   
    print("✅ Database initialized successfully!")

    
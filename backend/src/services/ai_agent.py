import os
from dotenv import load_dotenv
load_dotenv()

from typing_extensions import TypedDict

from src.configs.db_con import engine, SessionLocal, db, initialize_db

from langchain_groq import ChatGroq
from langchain import hub
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import StateGraph, END


initialize_db()
# langchain langchain-community langchain-core langgraph langchain-groq

print(db.dialect)



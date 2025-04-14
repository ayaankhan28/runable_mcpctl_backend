from fastapi import FastAPI
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
# from uuid import UUID
from sqlalchemy.dialects.postgresql import JSONB, UUID
from datetime import datetime

from sqlalchemy.orm import declarative_base, sessionmaker
from supabase import create_client, Client
from models.packages_models import *
from dotenv import load_dotenv
import os

load_dotenv()  # Loads from .env file

##
database_url = os.getenv("DATABASE_URL")
##
engine = create_engine(database_url)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

from sqlalchemy.orm import joinedload

def search_packages_by_name(session, search_term: str):
    if not search_term:
        packages = session.query(Packages)\
        .options(
            joinedload(Packages.inputs),
            joinedload(Packages.dependencies),  # Optional: remove if you don't need aliases
        )\
        .all()
    else:
        packages = session.query(Packages)\
            .options(
                joinedload(Packages.inputs),
                joinedload(Packages.dependencies),  # Optional: remove if you don't need aliases
            )\
            .filter(Packages.name.ilike(f"%{search_term}%"))\
            .all()

    return packages



app = FastAPI()


@app.get("/")
def health_check():
    return {"success": True}

@app.get("/get-package")
def get_package(package_name: Optional[str]= None):
    all_user = search_packages_by_name(session, package_name)
    return {"packages":all_user}
        



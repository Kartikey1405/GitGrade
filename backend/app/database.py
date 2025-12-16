from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# Get the URL from .env
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine (the core connection)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Create a Session factory (to talk to the DB)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models
Base = declarative_base()

# Dependency: This helper function gives a fresh database session for each request
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
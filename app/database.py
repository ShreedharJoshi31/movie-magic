import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is loaded successfully
if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in .env file")

# Create the database engine with connection pooling settings
engine = create_engine(
    DATABASE_URL,
    pool_size=150,
    max_overflow=0,
    pool_timeout=30,
    pool_recycle=7200,
    pool_pre_ping=True,
)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()

# Dependency for database session
def get_db():
    """
    Provides a database session and ensures it is closed after use.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

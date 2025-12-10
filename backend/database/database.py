from sqlalchemy import create_engine, Column, String, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from typing import Generator
import os
from dotenv import load_dotenv
import uuid
from sqlalchemy.sql import func


# Load environment variables
load_dotenv()

# Get database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/textbook_db")

# Create engine
engine = create_engine(DATABASE_URL)

# Create session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for models
Base = declarative_base()


# ORM Models
class SavedGenerationParameterSet(Base):
    __tablename__ = "saved_generation_parameter_sets"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=True)
    parameters = Column(JSON, nullable=False) # Stores the GenerateTextbookRequest.dict() as JSON
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

# Dependency to get database session
def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
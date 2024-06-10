# app/library/database.py

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from config import TEST_DATA_TABLE_URL

SQLALCHEMY_DATABASE_URL = TEST_DATA_TABLE_URL

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create the database tables
Base.metadata.create_all(bind=engine)

# database.py
from sqlmodel import create_engine, Session
from sqlalchemy.orm import sessionmaker

# Replace this with your actual database URL
from backend.config import CONNECTION_STRING

engine = create_engine(CONNECTION_STRING)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

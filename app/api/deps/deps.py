#standard FastAPI dependency for providing a database session to your routes

from app.db.session import SessionLocal
from sqlalchemy.orm import Session
from fastapi import Depends #FastAPI’s way to inject dependencies into route functions.

#Define the dependency
def get_db():
    db = SessionLocal() #Creates a new database session.
    try: #This is the FastAPI standard pattern for SQLAlchemy integration.
        yield db #This makes the function a generator.
    finally:
        db.close() #Ensures the database connection is closed no matter what happens in the route.
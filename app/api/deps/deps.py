#standard FastAPI dependency for providing a database session to my routes

from app.db.session import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
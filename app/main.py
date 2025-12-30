# .venv\Scripts\activate
# mysql -u root -p
# uvicorn app.main:app --reload
# USE fastapi_db;
# SHOW TABLES;
# redis-server
# celery -A app.core.celery_app.celery_app worker --pool=solo --loglevel=info

from fastapi import FastAPI
from app.api.routers import items, auth, email

app = FastAPI()

app.include_router(items.router)
app.include_router(auth.router)
app.include_router(email.router)

@app.get("/")
def read_root():
    return {"message" : "FastAPI is working!"}

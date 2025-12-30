1) FastAPI CRUD Project

This project demonstrates a clean and well-tested backend application using FastAPI, SQLAlchemy ORM, MySQL, Redis, Celery, JWT OAuth2.
It includes user authentication, item management, background email sending system, caching and hashing.


2) Features

**FastAPI Routing & Pydantic Models**
  - Defined routers for 'item', 'user', 'email'
  - Input validation and response serialization with Pydantic

**Database Integration**
  - SQLAlchemy ORM for MySQL
  - Alembic migrations (create, upgrade, and manage DB schema)
  - Models and schemas for Items, Users, Emails

**Authentication**
  - JWT OAuth2 password flow
  - Password hashing with 'passlib'

**CRUD Operations**
  - Create, read, update, delete items
  - Proper HTTP status codes and exceptions

**Background Tasks**
  - Celery + Redis for sending emails asynchronously
  - Task scheduling and database tracking
  - Integration with MailSlurp for testing email sending

**Caching**
  - Redis caching example for GET requests (items list)
  - Cache invalidation and TTL

**Logging & Error Handling**
  - Structured logging
  - Exception handling for FastAPI endpoints and Celery tasks

**Testing**
  - Basic tests for endpoints, database, and background tasks


3) Project Structure

app/
├─ api/
│ ├─ deps/
│ │ ├─ auth_deps.py
│ │ └─ deps.py
│ ├─ routers/
│ │ ├─ auth.py
│ │ ├─ email.py
│ │ └─ items.py
├─ core/
│ ├─ celery_app.py
│ ├─ redis_cache.py
│ └─ security.py
├─ db/
│ └─ session.py
├─ models/
│ ├─ email.py
│ ├─ item.py
│ └─ user.py
├─ schemas/
│ ├─ email.py
│ ├─ item.py
│ └─ user.py
└─ tasks/
│ └─ email_tasks.py
main.py


4) How to Run

Install dependencies: pip install -r requirements.txt
Set up MySQL and run Alembic migrations.
Start Redis server locally: redis-server
Activate Virtual Environment: .venv\Scripts\activate
Run FastAPI: uvicorn main:app --reload
Start Celery worker: celery -A app.core.celery_app.celery_app worker --loglevel=info
Access Swagger UI at http://127.0.0.1:8000/docs.

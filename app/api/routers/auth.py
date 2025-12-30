from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.api.deps.deps import get_db
from app.models.user import User as UserModel
from app.schemas.user import UserCreate, Users, UserLogin
from app.core import security

#Create a router tagged under "auth"
router = APIRouter(prefix="/auth", tags=["auth"])

#Register a new user
@router.post("/register", response_model=Users)
def register(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.username == user.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    db_user = UserModel(
        username = user.username,
        email = user.email,
        hashed_password = security.hash_password(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

#Login user & return JWT
@router.post("/login")
def login(
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # create Pydantic model from form data
    user_data = UserLogin(username=username, password=password)

    db_user = db.query(UserModel).filter(UserModel.username == user_data.username).first()
    if not db_user or not security.verify_password(user_data.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = security.create_access_token(data={"sub": db_user.username})
    return {"access_token": access_token, "token_type": "bearer"}
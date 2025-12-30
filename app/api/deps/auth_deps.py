#Create a dependency for getting the current user

from fastapi import Depends, HTTPException, status #HTTPException and status → used to throw standard HTTP errors
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError #library for encoding/decoding JSON Web Tokens.
from sqlalchemy.orm import Session #for accessing the database.

from app.api.deps.deps import get_db
from app.models.user import User
from app.core.security import SECRET_KEY, ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception

    return user
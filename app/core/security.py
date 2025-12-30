import os
import bcrypt

from passlib.context import CryptContext #secure password hashing library
from datetime import datetime, timedelta
from jose import jwt #encode/decode JSON Web Tokens (JWT)

"""
in Python Console:
import secrets
random_hex = secrets.token_hex(32)  # 32 bytes, or 64 hex characters
print(random_hex)
"""

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.environ["ALGORITHM"]
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
##bcrypt is the hashing algorithm (secure and standard).
#deprecated="auto" means if you ever change schemes, old passwords still work.


def hash_password(password: str) -> str:
    """
        Hash a password using bcrypt.
        Returns the hash as a UTF-8 string.
    """
    password_bytes = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

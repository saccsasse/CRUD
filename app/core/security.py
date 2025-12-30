#JWT-JSON Web Token - based authentication utility

import bcrypt

from jose.constants import ALGORITHMS #common list of algorithm constants
from passlib.context import CryptContext #secure password hashing library
from datetime import datetime, timedelta #handle expiration time for tokens.
from jose import jwt #encode/decode JSON Web Tokens (JWT)

"""
in Python Console:
import secrets
random_hex = secrets.token_hex(32)  # 32 bytes, or 64 hex characters
print(random_hex)
"""

SECRET_KEY = 'cc6c793f6cf9f30cf5ea8874b8584feef3fa667dd8e2d666fadf5a32a66dd4df'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 #default token lifetime = 60 minutes.

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
##bcrypt is the hashing algorithm (secure and standard).
#deprecated="auto" means if you ever change schemes, old passwords still work.

#Password hashing
def hash_password(password: str) -> str:
    """
        Hash a password using bcrypt.
        Returns the hash as a UTF-8 string.
    """
    password_bytes = password.encode('utf-8') #convert to bytes
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed.decode('utf-8') #store as string


#Compares the user’s entered password with the stored hash.
def verify_password(password: str, hashed: str) -> bool:
    """
        Verify a plain password against a hashed password.
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)

# JWT token creation
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy() #start with the payload
    expire = datetime.utcnow() + (expires_delta if expires_delta else timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) #calculate expiration timestamp. Default = 60 minutes.
    to_encode.update({"exp": expire}) #add the expiration time to the token payload.

    #create a signed JWT
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) #signed using SECRET_KEY.
    return encoded_jwt #eyJhbGciOiJIUzI1NiIsInR5cCI6Ikp9...

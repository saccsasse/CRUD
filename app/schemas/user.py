from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Users(UserBase):
    id: int
    model_config = { #Pydantic v2
        "from_attributes": True
    }

#class Config: #Pydantic v1
#   orm_mode = True
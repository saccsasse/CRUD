from pydantic import BaseModel, EmailStr
from datetime import datetime

class EmailCreate(BaseModel):
    recipient: EmailStr
    subject: str
    body: str

class EmailRead(EmailCreate):
    id: int
    sent: bool
    timestamp: datetime
    model_config = {
        "from_attributes": True
    }

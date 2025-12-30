from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from app.db.session import Base

class Email(Base):
    __tablename__ = "emails"

    id = Column(Integer, primary_key=True, index=True)
    recipient = Column(String(255), nullable=False)
    subject = Column(String(255), nullable=False)
    body = Column(String(255), nullable=False)
    sent = Column(Boolean, default=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
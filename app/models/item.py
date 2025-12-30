#Create your first model

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.db.session import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    price = Column(Float, nullable = False)
    owner_id = Column(Integer, ForeignKey("users.id"))  # new column
    owner = relationship("User", back_populates="items")
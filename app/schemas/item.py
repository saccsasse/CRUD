from pydantic import BaseModel

#Defining a Pydantic model :
#automatically converts types if possible and raises errors if the data is invalid
#parse incoming data like JSON into Python objects
#allows to set defaults

#Request body → validated Pydantic model
#Response → automatically converted to JSON
#OpenAPI docs → automatically generated from Pydantic models

class ItemBase(BaseModel):
    name: str
    description: str | None = None #should be a string OR none is default
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase): #Item response
    id: int #represents an item stored in the database that has a unique identifier
    model_config = {  # Pydantic v2
        "from_attributes": True
    }

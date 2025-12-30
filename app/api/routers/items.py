#Create the router = store
from fastapi import APIRouter, Depends, HTTPException #HTTPException → raise errors if needed.
from sqlalchemy.orm import Session

from app.schemas.item import Item, ItemCreate
from app.models.item import Item as ItemModel #SQLAlchemy model representing the database table.
from app.models.user import User
from app.api.deps.deps import get_db
from app.api.deps.auth_deps import get_current_user
from app.core.redis_cache import get_cache, set_cache, delete_cache

router = APIRouter(prefix="/items", tags=["items"]) #define a router, tags=["items"] is for Swagger UI

# List all items with Redis caching
@router.get("/", response_model=list[Item]) #response_model ensures FastAPI automatically serializes responses and validates output.
def list_items(db: Session = Depends(get_db)): #FastAPI automatically calls get_db() and gives a session.
    cache_key = "items_list"

    #Try fetching from Redis cache
    cached_items = get_cache(cache_key)
    if cached_items:
        print("Returning data from cache")
        return cached_items
    print("Cache miss - querying DB")

    items = db.query(ItemModel).all() #SQLAlchemy query that selects all rows from the items table.
    serialized = [Item.from_orm(item).dict() for item in items]
    set_cache(cache_key, serialized, ttl=60)
    return serialized

# Create a new item
@router.post("/", response_model=Item)
def create_item(
    item: ItemCreate, #item: ItemCreate → Parses JSON from the request body.
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_item = ItemModel(**item.model_dump(), owner_id=current_user.id) #converts Pydantic object to a dictionary, ** → unpacks the dictionary into the SQLAlchemy model.
    db.add(db_item) #stage the object for insertion into the database.
    db.commit() #save the changes to the database.
    delete_cache("items_list") #delete cache after some data change
    db.refresh(db_item)
    return db_item #FastAPI automatically converts the SQLAlchemy object to JSON, using Item schema because of response_model=Item.

# Get a single item by ID
@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id). first() #query a single row
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

# Update an item
@router.put("/{item_id}", response_model=Item)
def update_item(
    item_id: int,
    updated_item: ItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.name = updated_item.name
    item.description = updated_item.description
    item.price = updated_item.price

    db.commit() #commit changes
    delete_cache("items_list")
    db.refresh(item) #update fields
    return item

# Delete an item
@router.delete("/{item_id}", response_model=dict)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if item.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not allowed")
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    delete_cache("items_list")
    db.commit()
    return {"message" : f"Item {item_id} deleted successfully"}
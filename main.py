from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()
 
 # Add middleware to enable CORS
app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)
class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
 
items = []
 
@app.post("/items/", response_model=Item)
def create_item(item: Item):
    for existing_item in items:
        if existing_item.id == item.id:
            raise HTTPException(status_code=400, detail="Item with this ID already exists.")
    items.append(item)
    return item
 
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for idx, existing_item in enumerate(items):
        if existing_item.id == item_id:
            items[idx] = item
            return item
    raise HTTPException(status_code=404, detail="Item not found.")
 
@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for item in items:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found.")
 
@app.get("/items/", response_model=List[Item])
def read_items():
    return items
 
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

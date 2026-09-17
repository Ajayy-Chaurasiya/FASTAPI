from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Literal

app = FastAPI()

# ---------- Pydantic Models ----------

class MomoItem(BaseModel):
    name: str
    quantity: int = Field(gt=0, le=20)          # validation
    spice_level: Literal["mild", "medium", "hot"] = "medium"
    sauce: Literal["tomato", "sesame", "chutney"] = "tomato"

class Customer(BaseModel):
    name: str
    phone: str

class Order(BaseModel):
    customer: Customer          # nested model
    items: List[MomoItem]       # nested list of models

# ---------- Fake menu data ----------

menu = [
    {"name": "Steam Momo", "type": "veg", "price": 120},
    {"name": "Fried Momo", "type": "non-veg", "price": 150},
    {"name": "Jhol Momo", "type": "veg", "price": 130},
]

# ---------- Routes ----------

@app.get("/")
def home():
    return {"message": "Welcome to the Momo Order API"}

@app.get("/menu")
def get_menu(type: str = Query(default=None), max_price: int = Query(default=None)):
    result = menu
    if type:
        result = [m for m in result if m["type"] == type]
    if max_price:
        result = [m for m in result if m["price"] <= max_price]
    return {"menu": result}

@app.post("/order")
def place_order(order: Order):
    total = 0
    for item in order.items:
        price = next((m["price"] for m in menu if m["name"] == item.name), 0)
        total += price * item.quantity
    return {
        "customer": order.customer,
        "items_ordered": order.items,
        "total_price": total,
        "status": "Order placed!"
    }
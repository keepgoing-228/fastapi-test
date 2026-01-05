from fastapi import FastAPI, status, HTTPException
from app.schemas import OrderCreateInput, OrderUpdateInput
from uuid import uuid4

app = FastAPI()

# simple memory storage
orders_db = {}


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/orders/")
def get_all_orders():
    return {"orders": list(orders_db.values()), "total": len(orders_db)}


@app.get("/orders/{order_id}")
def get_order(order_id: int):
    """get an order by id"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return orders_db[order_id]


@app.post("/orders")
def create_order(data: OrderCreateInput):
    """create a new order"""

    # save the order to memory storage
    orders_db[data.id] = {"id": data.id, "name": data.name}

    return {"message": "Order created successfully"}


@app.put("/orders/{order_id}")
def update_order(order_id: int, data: OrderUpdateInput):
    """update an order by id"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    # update the order in memory storage
    orders_db[order_id]["name"] = data.name
    return orders_db[order_id]

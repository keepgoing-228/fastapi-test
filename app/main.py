from fastapi import FastAPI, HTTPException, Depends
from app.auth import OrderCreateInput, OrderUpdateInput
from uuid import UUID
from typing import Annotated


app = FastAPI()

# simple memory storage
orders_db = {
    "3fa85f64-5717-4562-b3fc-2c963f66afa6": {"name": "order 1", "number": 1},
}


@app.get("/")
def root():
    return {"message": "Hello FastAPI"}


@app.get("/orders/")
def get_all_orders():
    return {"orders": list(orders_db.values()), "total": len(orders_db)}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    """get an order by id"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")
    return orders_db[order_id]


@app.post("/orders")
def create_order(data: OrderCreateInput):
    """create a new order"""

    # save the order to memory storage
    orders_db[data.id] = {"name": data.name, "number": data.number}

    return {"message": "Order created successfully"}


@app.put("/orders/{order_id}")
def update_order(order_id: str, data: OrderUpdateInput):
    """update an order by id"""
    if order_id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order {order_id} not found")

    # update the order in memory storage
    orders_db[order_id]["name"] = data.name
    orders_db[order_id]["number"] = data.number
    return orders_db[order_id]


# Check if the order exists by using a dependency
def get_order_data(id: UUID) -> dict:
    id = str(id)
    if id not in orders_db:
        raise HTTPException(status_code=404, detail=f"Order {id} not found")
    return orders_db[id]


@app.get("/test")
def test_depends(test: Annotated[dict, Depends(get_order_data)]):
    return {"test": test}

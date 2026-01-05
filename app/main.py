from fastapi import FastAPI, HTTPException, Depends
from app.schemas import OrderCreateInput, OrderUpdateInput

app = FastAPI()

# simple memory storage
orders_db = {
    "1": {"name": "order 1", "number": 1},
    "2": {"name": "order 2", "number": 2},
    "3": {"name": "order 3", "number": 3},
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

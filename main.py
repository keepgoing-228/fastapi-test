from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get(f"/orders/")
def get_order(id: int = 5, name: str = "my order"):
    return {"id": id, "name": name}

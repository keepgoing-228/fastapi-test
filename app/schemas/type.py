from pydantic import BaseModel


class OrderCreateInput(BaseModel):
    id: int
    name: str


class OrderUpdateInput(BaseModel):
    name: str

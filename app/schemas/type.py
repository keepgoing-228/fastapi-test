from pydantic import BaseModel
from typing import Optional


class OrderCreateInput(BaseModel):
    id: str
    name: str
    number: Optional[int] = None


class OrderUpdateInput(BaseModel):
    name: str
    number: Optional[int] = None

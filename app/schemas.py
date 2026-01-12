### Schemas for Pydantic models ###

from pydantic import BaseModel, field_validator, Field, EmailStr
from datetime import datetime
from typing import Optional


class DateTimeBase(BaseModel):
    created_at: str
    updated_at: str

    @field_validator("created_at", "updated_at", mode="before")
    @classmethod
    def datetime_to_str(cls, v: datetime):
        if isinstance(v, datetime):
            return datetime.strftime(v, "%Y-%m-%d %H:%M:%S")
        return str(v)


class Customer(DateTimeBase):
    id: str
    customer_name: str
    model_config = {"from_attributes": True}


class CustomerCreateInput(BaseModel):
    customer_name: Optional[str] = Field(
        ..., min_length=1, max_length=30, title="Customer Name"
    )
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30, title="Password")


class LoginInput(BaseModel):
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=30, title="Password")


class LoginReturn(Customer):
    token: str


class ItemBase(DateTimeBase):
    id: str
    item_name: str
    price: float
    quantity: int

    model_config = {"from_attributes": True}


class ItemCreateInput(BaseModel):
    item_name: str
    price: float
    quantity: int


class ItemUpdateInput(BaseModel):
    item_name: Optional[str]
    price: Optional[float]
    quantity: Optional[int]


class OrderBase(DateTimeBase):
    id: str
    customer_id: str
    item_id: str
    quantity: int

    model_config = {"from_attributes": True}


class OrderCreateInput(BaseModel):
    item_id: str
    quantity: int

from fastapi import FastAPI, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session

from app import schemas, service, exceptions, dependencies
from app.database import get_db


app = FastAPI()


@app.post(
    "/customers",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Customer,
)
def create_customer(dependency=Depends(dependencies.check_new_customer)):
    customer, db = dependency
    return service.create_customer(db, customer)


@app.get("/customers/all", response_model=list[schemas.Customer | None])
def get_all_customers(db: Session = Depends(get_db)):
    return service.get_all_customers(db)


@app.get("/customers", response_model=schemas.Customer)
def get_customers_by_id(id: UUID, db: Session = Depends(get_db)):
    id = str(id)
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return customer


@app.patch("/customers", response_model=schemas.Customer)
def update_customer(
    id: UUID, update_data: schemas.CustomerCreateInput, db: Session = Depends(get_db)
):
    id = str(id)
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return service.update_customer(db, update_data, customer)


@app.delete(
    "/customers",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Customer not found"}},
)
def delete_customer(id: UUID, db: Session = Depends(get_db)):
    id = str(id)
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    service.delete_customer(db, customer)


@app.post("/login", response_model=schemas.Customer)
def login(customer: schemas.Customer = Depends(dependencies.authenticate_customer)):
    return customer

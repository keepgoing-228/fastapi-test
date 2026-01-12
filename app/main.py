from fastapi import FastAPI, Depends, status
from uuid import UUID
from sqlalchemy.orm import Session

from app import schemas, service, exceptions, dependencies, models, jwt
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


@app.get(
    "/customers/me",
    response_model=schemas.Customer,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Customer not found"}},
)
def get_current_customer(
    jwt_data: dict = Depends(jwt.decode_token), db: Session = Depends(get_db)
):
    id = jwt_data.get("sub")
    customer = service.get_customer_by_id(db, id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return customer


@app.patch("/customers/{id}", response_model=schemas.Customer)
def update_customer(
    id: UUID,
    update_data: schemas.CustomerCreateInput,
    jwt_data: dict = Depends(jwt.decode_token),
    db: Session = Depends(get_db),
):

    customer_id = str(id)
    current_customer_id = jwt_data.get("sub")

    if customer_id != current_customer_id:
        raise exceptions.UnauthorizedOperation()

    customer = service.get_customer_by_id(db, customer_id)
    if not customer:
        raise exceptions.CustomerNotFound()
    return service.update_customer(db, update_data, customer)


@app.delete(
    "/customers/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    responses={status.HTTP_404_NOT_FOUND: {"description": "Customer not found"}},
)
def delete_customer(
    id: UUID,
    jwt_data: dict = Depends(jwt.decode_token),
    db: Session = Depends(get_db),
):
    customer_id = str(id)
    current_customer_id = jwt_data.get("sub")

    if customer_id != current_customer_id:
        raise exceptions.UnauthorizedOperation()

    customer = service.get_customer_by_id(db, customer_id)
    if not customer:
        raise exceptions.CustomerNotFound()
    service.delete_customer(db, customer)


@app.post("/login", response_model=schemas.LoginReturn)
def login(customer: models.Customer = Depends(dependencies.authenticate_customer)):
    access_token = jwt.create_access_token(
        data={
            "sub": customer.id,
            "email": customer.email,
        }  # sub is the subject of the JWT token, email is defined by us (customer)
    )
    return schemas.LoginReturn(**customer.__dict__, token=access_token)

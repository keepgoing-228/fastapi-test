from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from app import schemas, service
from app.database import get_db


app = FastAPI()


@app.post(
    "/customers",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Customer,
)
def create_customer(
    customer: schemas.CustomerCreateInput, db: Session = Depends(get_db)
):
    return service.create_customer(db, customer)

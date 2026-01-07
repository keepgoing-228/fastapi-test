from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, service, exceptions


def check_new_customer(
    customer: schemas.CustomerCreateInput,
    db: Session = Depends(get_db),
) -> tuple[schemas.CustomerCreateInput, Session]:
    db_customer = service.get_customer_by_email(db, customer.email)
    if db_customer:
        raise exceptions.CustomerAlreadyExists()
    return customer, db

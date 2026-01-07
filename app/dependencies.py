from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, service, exceptions, utils, models


def check_new_customer(
    customer: schemas.CustomerCreateInput,
    db: Session = Depends(get_db),
) -> tuple[schemas.CustomerCreateInput, Session]:
    db_customer = service.get_customer_by_email(db, customer.email)
    if db_customer:
        raise exceptions.CustomerAlreadyExists()
    return customer, db


def authenticate_customer(
    data: schemas.LoginInput, db: Session = Depends(get_db)
) -> models.Customer:
    db_customer = service.get_customer_by_email(db, data.email)
    if not db_customer:
        raise exceptions.CustomerNotFound()
    if not utils.verify_password(data.password, db_customer.password):
        raise exceptions.InvalidPasswordOrEmail()
    return db_customer

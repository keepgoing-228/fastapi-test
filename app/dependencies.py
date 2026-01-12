from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app import schemas, service, exceptions, utils, models, jwt
from app.config import ADMIN_EMAIL, ADMIN_PASSWORD


def check_new_customer(
    customer: schemas.CustomerCreateInput,
    db: Session = Depends(get_db),
) -> tuple[schemas.CustomerCreateInput, Session]:
    db_customer = service.get_customer_by_email(db, customer.email)
    if db_customer:
        raise exceptions.CustomerAlreadyExists()
    return customer, db


def authenticate_customer(
    data: schemas.LoginInput,  # `data` is the request body
    db: Session = Depends(get_db),  # `db` is the database session
) -> models.Customer:
    db_customer = service.get_customer_by_email(db, data.email)
    if not db_customer:
        raise exceptions.CustomerNotFound()
    if not utils.verify_password(data.password, db_customer.password):
        raise exceptions.InvalidPasswordOrEmail()
    return db_customer


def check_new_item(
    item: schemas.ItemCreateInput,
    db: Session = Depends(get_db),
) -> tuple[schemas.ItemCreateInput, Session]:
    db_item = service.get_item_by_name(db, item.item_name)
    if db_item:
        raise exceptions.ItemAlreadyExists()
    return item, db


def authenticate_admin(data: schemas.LoginInput) -> bool:
    if data.email != ADMIN_EMAIL or data.password != ADMIN_PASSWORD:
        raise exceptions.InvalidPasswordOrEmail()
    return True


def check_is_admin(jwt_data: dict = Depends(jwt.decode_token)) -> bool:
    if jwt_data["sub"] != "admin":
        raise exceptions.NotAdmin()
    return True

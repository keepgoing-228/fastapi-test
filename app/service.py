from sqlalchemy.orm import Session, noload
from sqlalchemy import select
from app import schemas, exceptions, models, utils


def create_customer(
    db: Session, customer: schemas.CustomerCreateInput
) -> models.Customer:
    customer.password = utils.get_password_hash(customer.password)
    db_customer = models.Customer(**customer.model_dump())

    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except Exception as e:
        db.rollback()
        print(f"Error creating customer: {type(e).__name__}: {str(e)}")
        raise exceptions.ServerError(f"Error creating customer: {str(e)}")

    return db_customer


def get_all_customers(db: Session) -> list[models.Customer]:
    query = select(models.Customer).options(noload(models.Customer.orders))
    try:
        customers = db.execute(query).scalars().all()
    except Exception as e:
        raise exceptions.ServerError(f"Error getting all customers: {str(e)}")
    return customers


def get_customer_by_id(db: Session, id: str) -> models.Customer:
    query = select(models.Customer).where(models.Customer.id == id)
    try:
        customer = db.execute(query).scalar()
    except Exception as e:
        raise exceptions.ServerError(f"Error getting customer by id: {str(e)}")
    return customer


def get_customer_by_email(db: Session, email: str) -> models.Customer:
    query = select(models.Customer).where(models.Customer.email == email)
    try:
        customer = db.execute(query).scalar()
    except Exception as e:
        raise exceptions.ServerError(f"Error getting customer by email: {str(e)}")
    return customer


def update_customer(
    db: Session, update_data: schemas.CustomerCreateInput, customer: models.Customer
) -> models.Customer:
    update_data: dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(customer, key, value)
    try:
        db.commit()
        db.refresh(customer)
    except Exception as e:
        db.rollback()
        print(f"Error updating customer: {type(e).__name__}: {str(e)}")
        raise exceptions.ServerError(f"Error updating customer: {str(e)}")
    return customer


def delete_customer(db: Session, customer: models.Customer) -> None:
    try:
        db.delete(customer)
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error deleting customer: {type(e).__name__}: {str(e)}")
        raise exceptions.ServerError(f"Error deleting customer: {str(e)}")


def create_item(db: Session, item: schemas.ItemCreateInput):
    db_item = models.Item(**item.model_dump())

    db.add(db_item)
    try:
        db.commit()
        db.refresh(db_item)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error creating item")

    return db_item


def get_item_by_id(db: Session, id: str) -> models.Item:
    query = select(models.Item).where(models.Item.id == id)
    item = db.execute(query).scalar()
    return item


def get_item_by_name(db: Session, name: str) -> models.Item:
    query = select(models.Item).where(models.Item.item_name == name)
    item = db.execute(query).scalar()
    return item


def get_all_items(db: Session):
    query = select(models.Item)
    items = db.execute(query).scalars().all()
    return items


def update_item(
    db: Session, update_data: schemas.ItemUpdateInput, item: models.Item
) -> models.Item:
    update_data: dict = update_data.model_dump(exclude_unset=True, exclude_none=True)
    for key, value in update_data.items():
        setattr(item, key, value)

    try:
        db.commit()
        db.refresh(item)
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error updating item")

    return item


def delete_item(db: Session, item: models.Item):
    try:
        db.delete(item)
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise exceptions.ServerError("Error deleting item")

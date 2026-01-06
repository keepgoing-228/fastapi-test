from sqlalchemy.orm import Session, noload
from sqlalchemy import select
from app import schemas, exception, models


def create_customer(
    db: Session, customer: schemas.CustomerCreateInput
) -> models.Customer:
    db_customer = models.Customer(**customer.model_dump())

    db.add(db_customer)
    try:
        db.commit()
        db.refresh(db_customer)
    except Exception as e:
        db.rollback()
        print(f"Error creating customer: {type(e).__name__}: {str(e)}")
        raise exception.ServerError(f"Error creating customer: {str(e)}")

    return db_customer


def get_all_customers(db: Session) -> list[models.Customer]:
    query = select(models.Customer).options(noload(models.Customer.orders))
    customers = db.execute(query).scalars().all()
    return customers


def get_customer_by_id(db: Session, id: str) -> models.Customer:
    query = select(models.Customer).where(models.Customer.id == id)
    customer = db.execute(query).scalar()
    return customer

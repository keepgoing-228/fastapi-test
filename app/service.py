from sqlalchemy.orm import Session
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

from sqlalchemy import create_engine, String, DateTime, func, mapped_column
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from app.utils import generate_uuid

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    id = mapped_column(String, primary_key=True, default=generate_uuid)
    created_at = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at = mapped_column(
        DateTime(timezone=True), onupdate=func.now(), server_default=func.now()
    )


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

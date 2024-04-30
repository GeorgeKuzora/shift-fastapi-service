import logging
from datetime import date

from exceptions import DatabaseException
from models import Base, User
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

engine = create_engine("sqlite://", echo=True)

logger = logging.getLogger(__name__)


def generate_schema():
    try:
        Base.metadata.create_all(engine)
    except Exception as e:
        logger.critical("Can't create database schema", exc_info=True)
        raise DatabaseException from e


def create_fake_data():
    with Session(engine) as session:
        alice = User(
            name="Alice",
            password="password",
            sallary=10,
            next_promotion_date=date(year=2025, month=12, day=12),
        )
        session.add_all([alice])
        try:
            session.commit()
        except Exception as e:
            logger.critical(
                "can't commit changes into database", exc_info=True
            )
            raise DatabaseException from e


if __name__ == "__main__":
    generate_schema()
    create_fake_data()

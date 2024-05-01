import logging
from datetime import date

from exceptions import DatabaseException, DataNotFoundException
from models import Base, User
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

engine = create_engine("sqlite+pysqlite:///sqlite3.db", echo=True)

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
            salary=10,
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


def get_user_by_id(user_id: int) -> dict[str, str | int | date]:
    with Session(engine) as session:
        stmt = select(User).where(User.id == user_id)
        user = session.scalars(stmt).first()
        if user is None:
            logger.info(f"not found user with id: {user_id}")
            raise DataNotFoundException
        return user.to_dict()


if __name__ == "__main__":
    get_user_by_id(1)

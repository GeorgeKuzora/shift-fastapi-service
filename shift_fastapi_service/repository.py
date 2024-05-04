import logging
from datetime import date

from passlib.context import CryptContext
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session

from exceptions import DatabaseException, DataNotFoundException
from models import Base, User

engine = create_engine("sqlite+pysqlite:///sqlite3.db", echo=True)

logger = logging.getLogger(__name__)


class Repository:

    def generate_schema(self):
        try:
            Base.metadata.create_all(engine)
        except Exception as e:
            logger.critical("Can't create database schema", exc_info=True)
            raise DatabaseException from e

    def create_fake_data(self):
        pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        with Session(engine) as session:
            alice = User(
                username="alice",
                email="alice@example.com",
                salary=10,
                next_promotion_date=date(year=2025, month=12, day=12),
                disabled=False,
                hashed_password=pwd_context.hash("alice12345"),
            )
            session.add_all([alice])
            try:
                session.commit()
            except Exception as e:
                logger.critical(
                    "can't commit changes into database", exc_info=True
                )
                raise DatabaseException from e

    def get_user_by_id(self, user_id: int) -> dict:
        with Session(engine) as session:
            stmt = select(User).where(User.id == user_id)
            user = session.scalars(stmt).first()
            if user is None:
                logger.info(f"not found user with id: {user_id}")
                raise DataNotFoundException
            return user.to_dict()

    def get_user_by_username(self, username: str) -> dict:
        with Session(engine) as session:
            stmt = select(User).where(User.username == username)
            user = session.scalars(stmt).first()
            if user is None:
                logger.info(f"not found user with username: {username}")
                raise DataNotFoundException
            return user.to_dict()


if __name__ == "__main__":
    db = Repository()
    db.generate_schema()
    db.create_fake_data()
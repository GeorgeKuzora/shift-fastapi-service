import logging
from datetime import date

from sqlalchemy import Date, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(40))
    password: Mapped[str] = mapped_column(String(50))
    salary: Mapped[int] = mapped_column(Integer())
    next_promotion_date: Mapped[date] = mapped_column(Date())

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r})"

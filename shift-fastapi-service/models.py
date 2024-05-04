from datetime import date

from sqlalchemy import Boolean, Date, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(50))
    salary: Mapped[int] = mapped_column(Integer())
    next_promotion_date: Mapped[date] = mapped_column(Date())
    disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    hashed_password: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.username!r})"

    def to_dict(self) -> dict[str, str | int | date]:
        return {
            "name": self.username,
            "salary": self.salary,
            "next_promotion_date": self.next_promotion_date,
        }

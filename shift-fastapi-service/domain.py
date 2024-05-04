from datetime import date

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class UserSalary(BaseModel):
    username: str
    salary: int


class UserNextPromotionDate(BaseModel):
    username: str
    next_promotion_date: date


class User(BaseModel):
    username: str
    email: str | None = None
    salary: int
    next_promotion_date: date
    disabled: bool = False

    def get_salary(self) -> UserSalary:
        return UserSalary(username=self.username, salary=self.salary)

    def get_next_promotion_date(self) -> UserNextPromotionDate:
        return UserNextPromotionDate(
            username=self.username,
            next_promotion_date=self.next_promotion_date,
        )


class UserInDB(User):
    hashed_password: str

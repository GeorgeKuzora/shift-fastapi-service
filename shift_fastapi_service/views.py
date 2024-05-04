import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse

from app import app
from auth.auth import get_current_active_user
from domain import User, UserNextPromotionDate, UserSalary
from exceptions import DataNotFoundException

logger = logging.getLogger(__name__)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/404")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
async def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}


@app.get("/user/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    return current_user


@app.get("/salary/me", response_model=UserSalary)
async def get_salary_for_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserSalary:
    user_salary: UserSalary = current_user.get_salary()
    return user_salary


@app.get("/promotion/me", response_model=UserNextPromotionDate)
async def get_next_promotion_date_for_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserNextPromotionDate:
    user_next_promotion_date: UserNextPromotionDate = (
        current_user.get_next_promotion_date()
    )
    return user_next_promotion_date

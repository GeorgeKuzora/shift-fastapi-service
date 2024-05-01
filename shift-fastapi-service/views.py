import logging
from datetime import date

from app import app
from exceptions import DataNotFoundException
from fastapi import HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse
from repository import get_user_by_id

logger = logging.getLogger(__name__)


@app.exception_handler(404)
async def not_found_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/404")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
async def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}


@app.get("/salary/{user_id}")
async def get_salary_by_user_id(
    user_id: int,
) -> Response:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException as e:
        logger.info(f"not found user with id: {user_id}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from e
    return {"user": user.get("name", ""), "salary": user.get("salary", 0)}


@app.get("/promotion/{user_id}")
async def get_next_promotion_date_by_user_id(
    user_id: int,
) -> Response:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException as e:
        logger.info(f"not found user with id: {user_id}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from e
    return {
        "user": user.get("name", ""),
        "next_promotion_date": user.get(
            "next_promotion_date", date(year=1, month=1, day=1)
        ),
    }

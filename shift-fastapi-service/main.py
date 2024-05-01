import logging
from datetime import date

from exceptions import DataNotFoundException
from fastapi import FastAPI, Request, Response, status
from fastapi.responses import RedirectResponse
from logs import init_logging
from repository import get_user_by_id

init_logging()
logger = logging.getLogger(__name__)

app = FastAPI()


@app.exception_handler(404)
def not_found_handler(request: Request, exc: Exception):
    return RedirectResponse(url="/404")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}


@app.get("/")
def read_root() -> dict[str, str]:
    return {"Hello": "World"}


@app.get("/salary/{user_id}")
def get_salary_by_user_id(
    user_id: int,
) -> Response:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException:
        logger.info(f"not found user with id: {user_id}", exc_info=True)
        return RedirectResponse(
            url="/404", status_code=status.HTTP_404_NOT_FOUND
        )
    return {"user": user.get("name", ""), "salary": user.get("salary", 0)}


@app.get("/promotion/{user_id}")
def get_next_promotion_date_by_user_id(
    user_id: int,
) -> Response:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException:
        logger.info(f"not found user with id: {user_id}", exc_info=True)
        return RedirectResponse(
            url="/404", status_code=status.HTTP_404_NOT_FOUND
        )
    return {
        "user": user.get("name", ""),
        "next_promotion_date": user.get(
            "next_promotion_date", date(year=1, month=1, day=1)
        ),
    }

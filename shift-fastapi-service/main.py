import logging

from exceptions import DataNotFoundException
from fastapi import FastAPI, status
from repository import get_user_by_id

logging.basicConfig(filename="logs/main.log", level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
def not_found() -> dict[str, str]:
    return {"message": "Resource Not Found"}


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/salary/{user_id}")
def get_salary_by_user_id(
    user_id: int,
) -> dict[str, str] | dict[str, str | int | date]:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException:
        logger.info(f"not found user with id: {user_id}", exc_info=True)
        return not_found()
    response = {"user": user.get("name", ""), "salary": user.get("salary", 0)}
    return response

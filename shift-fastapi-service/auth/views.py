import logging
from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from app import app
from exceptions import DataNotFoundException
from fastapi import Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from repository import get_user_by_id, get_user_by_username

logger = logging.getLogger(__name__)


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user


@app.get("/users/me/items/")
async def read_own_items(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return [{"item_id": "Foo", "owner": current_user.username}]


@app.get("/salary/me")
async def get_salary_for_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> Response:
    try:
        user = get_user_by_id(user_id)
    except DataNotFoundException as e:
        logger.info(f"not found user with id", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from e
    return {"user": user.get("name", ""), "salary": user.get("salary", 0)}

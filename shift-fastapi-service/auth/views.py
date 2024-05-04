import logging
import os
from datetime import timedelta
from typing import Annotated

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app import app
from auth.auth import authenticate_user, create_access_token
from domain import Token
from repository import Repository

load_dotenv()
logger = logging.getLogger(__name__)

env_var = os.environ

DEFAULT_ACCESS_TOKEN_EXPIRE_TIME = 15.0
ACCESS_TOKEN_EXPIRE_TIME: str | None = env_var.get(
    "ACCESS_TOKEN_EXPIRE_MINUTES"
)

try:
    ACCESS_TOKEN_EXPIRE_MINUTES = float(ACCESS_TOKEN_EXPIRE_TIME)
except TypeError:
    logger.error(
        f"ACCESS_TOKEN_EXPIRE_MINUTES {ACCESS_TOKEN_EXPIRE_TIME} was not provided, set to {DEFAULT_ACCESS_TOKEN_EXPIRE_TIME}"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: float = DEFAULT_ACCESS_TOKEN_EXPIRE_TIME
except ValueError:
    logger.error(
        f"ACCESS_TOKEN_EXPIRE_MINUTES {ACCESS_TOKEN_EXPIRE_TIME} is not an integer, set to {DEFAULT_ACCESS_TOKEN_EXPIRE_TIME}"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES = DEFAULT_ACCESS_TOKEN_EXPIRE_TIME


@app.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Token:
    db = Repository()
    user = authenticate_user(db, form_data.username, form_data.password)
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

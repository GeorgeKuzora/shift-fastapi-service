import logging
import os
from datetime import date, datetime, timedelta, timezone
from typing import Annotated

from exceptions import AuthConfigException
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from repository import get_user_by_username

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

env_var = os.environ
SECRET_KEY: str | None = env_var.get("SECRET_KEY")
ALGORITHM: str | None = env_var.get("ALGORITHM")
if not SECRET_KEY or ALGORITHM:
    logger.error("secret key or algorithm was not provided")
    raise AuthConfigException("secret key or algorithm was not provided")

if ACCESS_TOKEN_EXPIRE_MINUTES := env_var.get("ACCESS_TOKEN_EXPIRE_MINUTES"):
    try:
        ACCESS_TOKEN_EXPIRE_MINUTES = int(ACCESS_TOKEN_EXPIRE_MINUTES)
    except ValueError:
        logger.error(
            f"ACCESS_TOKEN_EXPIRE_MINUTES {ACCESS_TOKEN_EXPIRE_MINUTES} is not an integer"
        )
        raise AuthConfigException(
            f"ACCESS_TOKEN_EXPIRE_MINUTES {ACCESS_TOKEN_EXPIRE_MINUTES} is not an integer"
        )


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


class User(BaseModel):
    username: str
    email: str | None = None
    salary: int | None = None
    next_promotion_date: date | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_user(db, username: str):
    user_dict = db(username)
    return UserInDB(**user_dict)


def authenticate_user(db, username: str, password: str):
    user = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(get_user_by_username, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

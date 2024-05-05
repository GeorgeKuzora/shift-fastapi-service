import logging
import os
from datetime import datetime, timedelta, timezone
from typing import Annotated, Literal

from dotenv import load_dotenv
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from shift_fastapi_service.domain import TokenData, User, UserInDB
from shift_fastapi_service.exceptions import (
    AuthConfigException,
    DataNotFoundException,
)
from shift_fastapi_service.repository import Repository

load_dotenv()
logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY: str | None = os.environ.get("SECRET_KEY")
ALGORITHM: str | None = os.environ.get("ALGORITHM")

if not SECRET_KEY:
    logger.error("secret key was not provided")
    raise AuthConfigException("secret key was not provided")

if not ALGORITHM:
    logger.error("algorithm was not provided")
    raise AuthConfigException("algorithm was not provided")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def get_user(db: Repository, username: str) -> UserInDB:
    try:
        user_dict: dict = db.get_user_by_username(username)
    except DataNotFoundException as e:
        logger.info(
            f"user with username {username} was not found",
            exc_info=True,
        )
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        ) from e
    return UserInDB(**user_dict)


def authenticate_user(
    db: Repository, username: str, password: str
) -> UserInDB | Literal[False]:
    user: UserInDB = get_user(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(
    data: dict, expires_delta: timedelta | None = None
) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(tz=timezone.utc) + expires_delta
    else:
        expire = datetime.now(tz=timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, key=SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, str] = jwt.decode(
            token=token, key=SECRET_KEY, algorithms=[ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user: UserInDB | None = None
    if token_data.username:
        db = Repository()
        user = get_user(db=db, username=token_data.username)
    else:
        raise credentials_exception
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

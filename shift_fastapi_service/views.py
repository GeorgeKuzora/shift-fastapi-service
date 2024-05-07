import logging
from typing import Annotated

from fastapi import Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse

from shift_fastapi_service.app import app
from shift_fastapi_service.auth.auth import (
    get_current_active_user,
    get_password_hash,
)
from shift_fastapi_service.domain import (
    User,
    UserNextPromotionDate,
    UserNotInDB,
    UserSalary,
)
from shift_fastapi_service.exceptions import NotUniqueException
from shift_fastapi_service.repository import Repository

logger = logging.getLogger(__name__)


@app.exception_handler(404)
async def not_found_handler(
    request: Request, exc: Exception
) -> RedirectResponse:
    """
    Exception handler for handling 404 error code.

    Args:
        request (Request): HTTP Request
        exc (Exception): HTTP Exception with status 404

    Returns:
        RedirectResponse: Redirects to page /404
    """
    return RedirectResponse(url="/404")


@app.get("/404", status_code=status.HTTP_404_NOT_FOUND)
async def not_found() -> dict[str, str]:
    """
    View for page /404

    Returns:
        dict[str, str]: json object with "message" field
    """
    return {"message": "Resource Not Found"}


@app.get("/user/me", response_model=User)
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> User:
    """
    View to request logged user data.

    Args:
        current_user (Annotated[User, Depends): User credentials

    Returns:
        User: Json object obtained by marshaling the User object
    """
    return current_user


@app.get("/salary/me", response_model=UserSalary)
async def get_salary_for_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserSalary:
    """
    View to request logged user salary data.

    Args:
        current_user (Annotated[User, Depends): User credentials

    Returns:
        UserSalary: Json object obtained by marshaling the UserSalary object
    """
    user_salary: UserSalary = current_user.get_salary()
    return user_salary


@app.get("/promotion/me", response_model=UserNextPromotionDate)
async def get_next_promotion_date_for_current_user(
    current_user: Annotated[User, Depends(get_current_active_user)],
) -> UserNextPromotionDate:
    """
    View to request logged user next promotion date data.

    Args:
        current_user (Annotated[User, Depends): User credentials

    Returns:
        UserSalary: Json object obtained by marshaling
                    the UserNextPromotionDate  object
    """
    user_next_promotion_date: UserNextPromotionDate = (
        current_user.get_next_promotion_date()
    )
    return user_next_promotion_date


@app.get("/create_schema")
async def create_schema() -> Response:
    """
    Utility view for generating database schema.

    Returns:
        Response: HTTP Response with HTTP status 201
    """
    db = Repository()
    db.generate_schema()
    return Response(status_code=status.HTTP_201_CREATED)


@app.get("/load_data")
async def load_data() -> Response:
    """
    Utility view for adding test data for test purposes.

    Returns:
        Response: HTTP Response with HTTP status 201
    """
    db = Repository()
    db.create_fake_data()
    return Response(status_code=status.HTTP_201_CREATED)


@app.post(path="/user/create")
async def create_user(user: UserNotInDB) -> Response:
    hashed_password: str = get_password_hash(user.password)
    user_dict = user.to_dict()
    user_dict["hashed_password":hashed_password]

    db = Repository()
    try:
        db.create_user(user_dict)
    except NotUniqueException:
        logger.info(
            f"user {user.username} or user with email {user.email} already exists"
        )
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="username or email already exists",
        )
    return Response(status_code=status.HTTP_201_CREATED)

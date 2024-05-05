from datetime import date
from typing import Literal
from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

import shift_fastapi_service.auth.auth as auth
from shift_fastapi_service.domain import UserInDB
from shift_fastapi_service.exceptions import DataNotFoundException
from shift_fastapi_service.repository import Repository


class TestHashVerifyPassword:

    PLAIN_PASSWORD = "PlainPassword12345"

    @pytest.fixture
    def hashed_password(self) -> str:
        return auth.get_password_hash(self.PLAIN_PASSWORD)

    @pytest.fixture
    def password_verified(self, hashed_password: str) -> bool:
        return auth.verify_password(
            plain_password=self.PLAIN_PASSWORD, hashed_password=hashed_password
        )

    @pytest.fixture
    def password_not_verified(self, hashed_password: str) -> bool:
        wrong_password = "not" + self.PLAIN_PASSWORD
        return auth.verify_password(
            plain_password=wrong_password, hashed_password=hashed_password
        )

    def test_hash_password_verified(self, password_verified: bool) -> None:
        assert password_verified is True

    def test_hash_password_not_verified(
        self, password_not_verified: bool
    ) -> None:
        assert password_not_verified is False


TEST_USER: dict = {
    "username": "alice",
    "email": "alice@alice.com",
    "salary": 10,
    "next_promotion_date": date(year=2025, month=12, day=12),
    "disabled": False,
    "hashed_password": "sdfadfsd93bkadskfjs923bzsa",
}

TEST_USER_IN_DB = UserInDB(**TEST_USER)


class TestGetUser:

    @pytest.fixture
    def user_and_db_for_validation(self) -> tuple[UserInDB, Repository]:
        db = Repository()
        db.get_user_by_username = MagicMock(return_value=TEST_USER)
        return auth.get_user(db, TEST_USER["username"]), db

    def test_get_valid_user(
        self, user_and_db_for_validation: tuple[UserInDB, Repository]
    ) -> None:
        valid_user, db = user_and_db_for_validation
        assert valid_user.username == TEST_USER["username"]
        assert valid_user.hashed_password == TEST_USER["hashed_password"]
        db.get_user_by_username.assert_called_once_with(TEST_USER["username"])

    @pytest.fixture
    def db_with_side_effect(self) -> Repository:
        db = Repository()
        db.get_user_by_username = MagicMock(side_effect=DataNotFoundException)
        return db

    def test_data_not_found_raises(
        self, db_with_side_effect: Repository
    ) -> None:
        with pytest.raises(HTTPException):
            auth.get_user(db_with_side_effect, TEST_USER["username"])


class TestAuthenticateUser:

    def get_user_with_auth_state(
        self, state: bool = True
    ) -> UserInDB | Literal[False]:
        db: Repository = Repository()
        password = "alice"
        with patch(
            "shift_fastapi_service.auth.auth.get_user", autospec=True
        ) as mock_get_user:
            mock_get_user.return_value = TEST_USER_IN_DB
            with patch(
                "shift_fastapi_service.auth.auth.verify_password",
                autospec=True,
            ) as mock_verify_password:
                mock_verify_password.return_value = state
                return auth.authenticate_user(
                    db, TEST_USER["username"], password
                )

    @pytest.fixture
    def authenticated_user(self) -> UserInDB | Literal[False]:
        return self.get_user_with_auth_state(state=True)

    @pytest.fixture
    def not_authenticated_user(self) -> UserInDB | Literal[False]:
        return self.get_user_with_auth_state(state=False)

    def test_authenticated_user_is_valid(
        self, authenticated_user: UserInDB
    ) -> None:
        assert isinstance(authenticated_user, UserInDB)
        assert authenticated_user.username == TEST_USER_IN_DB.username
        assert (
            authenticated_user.hashed_password
            == TEST_USER_IN_DB.hashed_password
        )

    def test_not_authenticated_user(
        self, not_authenticated_user: UserInDB
    ) -> None:
        assert not_authenticated_user is False

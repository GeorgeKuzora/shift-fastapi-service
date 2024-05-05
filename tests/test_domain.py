from datetime import date

import pytest

import shift_fastapi_service.domain as d


class TestUser:
    @pytest.fixture
    def test_user(self) -> d.User:
        return d.User(
            username="alice",
            email="alice@alice.com",
            salary=10,
            next_promotion_date=date(
                year=2025,
                month=12,
                day=12,
            ),
            disabled=False,
        )

    @pytest.fixture
    def user_salary(self, test_user: d.User) -> d.UserSalary:
        return test_user.get_salary()

    def test_salary_is_user_salary_type(
        self, user_salary: d.UserSalary
    ) -> None:
        assert isinstance(user_salary, d.UserSalary)

    def test_salary_has_required_fields(
        self, user_salary: d.UserSalary, test_user: d.User
    ) -> None:
        assert user_salary.username == test_user.username
        assert user_salary.salary == test_user.salary

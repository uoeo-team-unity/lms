import pytest

from lms.domains import UserService
from tests.factories import UserFactory


@pytest.mark.usefixtures("wipe_users_table")
class TestUserService:
    def test_create_user(self) -> None:
        # Test creating a user using the UserService
        user = UserFactory.build()
        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        message, status = UserService().create(params=params)

        assert message == f"User with email {user.email} successfully created"
        assert status == 201

    def test_create_user_with_missing_params(self) -> None:
        # Test creating a user with missing parameters
        user = UserFactory.build()
        params = {
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        message, status = UserService().create(params=params)

        assert message == "Something doesn't look right, please double check the parameters and try again"
        assert status == 422

    def test_create_user_with_same_email_address(self) -> None:
        # Test creating a user with an existing email address
        user = UserFactory.create()
        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        message, status = UserService().create(params=params)

        assert message == (
            f"User with email {user.email} already exists, " "please double check the parameters and try again"
        )
        assert status == 422

    def test_create_user_with_invalid_role(self) -> None:
        # Test creating a user with an invalid role
        user = UserFactory.build()
        params = {
            "username": user.username,
            "password": user.password,
            "role": "invalid",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        message, status = UserService().create(params=params)

        assert message == "You've specified an invalid role, please double check the parameters and try again"
        assert status == 422

    def test_user_login(self) -> None:
        # Test user login
        hashed_password = "$2b$12$nWgf5G0gVy.gTz2vK2IPSe.PeCHr2yRZPybuLY19ZOC9qlavSVi7y"  # equals to `test`
        user = UserFactory.create(password=hashed_password)
        message, status = UserService().login(username=user.username, password="test")

        assert message == "Successfully logged-in"
        assert status == 200

    def test_user_login_with_invalid_username(self) -> None:
        # Test user login with an invalid username
        hashed_password = "$2b$12$nWgf5G0gVy.gTz2vK2IPSe.PeCHr2yRZPybuLY19ZOC9qlavSVi7y"  # equals to `test`
        UserFactory.create(password=hashed_password)
        message, status = UserService().login(username="Invalid Username", password="test")

        assert (
            message == "An error occurred while trying to log-in, please double check your credentials and try again."
        )
        assert status == 422

    def test_user_login_with_invalid_password(self) -> None:
        # Test user login with an invalid password
        hashed_password = "$2b$12$nWgf5G0gVy.gTz2vK2IPSe.PeCHr2yRZPybuLY19ZOC9qlavSVi7y"  # equals to `test`
        user = UserFactory.create(password=hashed_password)
        message, status = UserService().login(username=user.username, password="invalid")

        assert (
            message == "An error occurred while trying to log-in, please double check your credentials and try again."
        )
        assert status == 422

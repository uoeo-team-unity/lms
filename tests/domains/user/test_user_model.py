import pytest
from lms.domains import User
from tests.factories import UserFactory

@pytest.mark.usefixtures("wipe_users_table")
class TestUserModel:
    def test_user_init(self) -> None:
        # Test initializing a User model
        user = UserFactory.build()
        assert isinstance(user, User)
        assert isinstance(user.first_name, str)
        assert isinstance(user.last_name, str)
        assert isinstance(user.email, str)
        assert isinstance(user.role_id, int)

    def test_user_init_with_missing_value(self) -> None:
        # Test initializing a User model with missing values
        with pytest.raises(TypeError) as error:
            User()

        assert str(error.value) == (
            "__init__() missing 7 required positional arguments: 'username', 'password', "
            "'role_id', 'first_name', 'last_name', 'email', and 'auth_token'"
        )

    def test_user_create(self) -> None:
        # Test creating a User model
        user = UserFactory.build()
        created_user = User.create(
            username=user.username,
            password=user.password,
            role_id=1,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            auth_token=user.auth_token,
        )

        assert isinstance(created_user, User)
        assert created_user.first_name == user.first_name
        assert created_user.last_name == user.last_name
        assert created_user.email == user.email

    def test_user_update(self) -> None:
        # Test updating a User model
        user = UserFactory.create()
        updated_user = user.update({"first_name": "updated name"})
        assert isinstance(updated_user, User)
        assert updated_user.first_name == "updated name"

    def test_user_update_if_email_already_exists_rollback(self) -> None:
        # Test updating a User model with an existing email (should trigger a rollback)
        user = UserFactory.create()
        another_user = UserFactory.create()

        with pytest.raises(ValueError):
            another_user.update({"email": user.email})

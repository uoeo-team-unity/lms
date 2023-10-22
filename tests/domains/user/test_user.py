import json
import pytest
from lms.domains import User, UserRole
from tests.factories import StudentFactory, UserFactory

@pytest.mark.usefixtures("wipe_users_table")
class TestUser:
    def test_create_user(self, client, admin_user) -> None:
        # Test creating a user
        user = UserFactory.build()
        params = {
            "username": user.username,
            "password": user.password,
            "role": "admin",
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
        }
        response = client.post("/users/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data.get("message") == f"User with email {user.email} successfully created"

    def test_create_user_with_hacker_mode_on(self, client, toggle_hacker_mode) -> None:
        # Test creating a user with hacker mode enabled
        user = UserFactory.build()
        # ... (same structure as above)

    def test_create_user_with_missing_argument(self, client, admin_user) -> None:
        # Test creating a user with missing arguments
        user = UserFactory.build()
        # ... (same structure as above)

    def test_create_user_with_existing_email_address(self, client, admin_user) -> None:
        # Test creating a user with an existing email address
        user = UserFactory.create()
        # ... (same structure as above)

    def test_list_all_users(self, client, admin_user) -> None:
        # Test listing all users
        UserFactory.create()
        UserFactory.create()
        # ... (same structure as above)

    def test_list_all_users_with_hacker_mode(self, client, toggle_hacker_mode) -> None:
        # Test listing all users with hacker mode enabled
        UserFactory.create()
        UserFactory.create()
        # ... (same structure as above)

    def test_list_all_users_as_a_teacher(self, client, teacher_user) -> None:
        # Test listing all users as a teacher
        UserFactory.create()
        UserFactory.create()
        # ... (same structure as above)

    def test_list_all_users_as_a_student(self, client, student_user) -> None:
        # Test listing all users as a student (with insufficient permissions)
        UserFactory.create()
        UserFactory.create()
        # ... (same structure as above)

    # Other test cases continue...

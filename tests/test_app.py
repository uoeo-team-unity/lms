import json
import os

# Import the AUTH_TOKEN_PATH from the test configuration.
from tests.conftest import AUTH_TOKEN_PATH


# Define a test class for the Flask application.
class TestApp:
    # Test the root endpoint of the application.
    def test_root(self, client) -> None:
        response = client.get("/")
        data = json.loads(response.data)

        # Assert that the response status code is 200 and that the response data is structured as expected.
        assert response.status_code == 200
        assert isinstance(data, dict)
        assert "message" in data
        assert "status" in data
        assert data["message"] == "hi!"
        assert data["status"] == "up"

    # Test the login functionality.
    def test_login(self, client, admin_user) -> None:
        username = "john"
        password = "password"

        # Prepare registration data for a new user and create that user via a POST request.
        params = {
            "username": username,
            "password": password,
            "role": "admin",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@test.com",
        }
        client.post("/users/create", json=params)

        # Attempt to log in with the new user's credentials and verify the response.
        response = client.post("/login", json={"username": username, "password": password})
        data = json.loads(response.data)

        # Assert that the response status code is 200 and that the login was successful.
        assert response.status_code == 200
        assert data == {"message": "Successfully logged-in"}

    # Test logging in with an invalid password.
    def test_login_with_invalid_password(self, client) -> None:
        username = "john"
        password = "password"

        # Prepare registration data for a new user and create that user via a POST request.
        params = {
            "username": username,
            "password": password,
            "role": "admin",
            "first_name": "John",
            "last_name": "Smith",
            "email": "john@test.com",
        }
        client.post("/users/create", json=params)

        # Attempt to log in with the new user's credentials and an invalid password, then verify the response.
        response = client.post("/login", json={"username": username, "password": "invalid_password"})
        data = json.loads(response.data)

        # Assert that the response status code is 422 and indicates a login error.
        assert response.status_code == 422
        assert data == {
            "message": "An error occurred while trying to log-in, please double-check your credentials and try again."
        }

    # Test logging in with invalid user credentials.
    def test_login_with_invalid_user(self, client) -> None:
        username = "jack"
        password = "password"

        # Attempt to log in with an invalid user's credentials and verify the response.
        response = client.post("/login", json={"username": username, "password": password})
        data = json.loads(response.data)

        # Assert that the response status code is 422 and indicates a login error.
        assert response.status_code == 422
        assert data == {
            "message": "An error occurred while trying to log-in, please double-check your credentials and try again."
        }

    # Test the logout functionality.
    def test_logout(self, client, admin_user) -> None:
        # Check if the AUTH_TOKEN_PATH file exists (indicating a user is logged in).
        assert os.path.exists(AUTH_TOKEN_PATH)

        # Log out the user and verify the response and file existence.
        response = client.put("/logout")
        data = json.loads(response.data)

        # Assert that the response status code is 200, the logout was successful,
        # and the AUTH_TOKEN_PATH file no longer exists.
        assert response.status_code == 200
        assert data == {"message": "Successfully logged-out of the app"}
        assert not os.path.exists(AUTH_TOKEN_PATH)

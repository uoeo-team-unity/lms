# Import necessary modules for file and random operations.
import os
import secrets

# Import types for code clarity and static type checking.
from typing import Final, Literal

# Import bcrypt library for password hashing.
import bcrypt

# Import User and UserRole classes from the user_model module within the same package.
from .user_model import User, UserRole

# Determine and set the path for the current file.
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


# Create the UserService class to handle user-related operations.
class UserService:
    # Define a method to create a new user.
    def create(self, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[201]]:
        # Extract user details from the input parameters.
        username = params.get("username")
        password = params.get("password")
        role = params.get("role")
        first_name = params.get("first_name")
        last_name = params.get("last_name")
        email = params.get("email")

        # Ensure all required parameters are present.
        if not all([username, password, role, first_name, last_name, email]):
            return "Something doesn't look right, please double check the parameters and try again", 422

        # Check if a user with the given email already exists.
        user = User.find_by(email=email)
        if user:
            return f"User with email {email} already exists, please double check the parameters and try again", 422

        # Convert role string to its corresponding enum value.
        try:
            role_id = UserRole[role.upper()].value
        except KeyError:
            return "You've specified an invalid role, please double check the parameters and try again", 422

        # Hash the user's password.
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        # Save the new user in the database.
        User.create(
            username=username,
            password=hashed_password.decode("utf-8"),
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            auth_token=secrets.token_hex(24),
        )

        return f"User with email {email} successfully created", 201

    # Define a method to update existing user information.
    def update(self, user_id: int, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[200]]:
        # Default error message and status code.
        message = "An error occurred while trying to update the user, please try again"
        status_code = 422

        # Fetch the user using the given ID.
        user = User.get(user_id)

        # Extract the role from the input parameters.
        role = params.get("role")

        # Return an error if the user is not found.
        if not user:
            return "We couldn't find the specified user, please try again", 422

        # If role is provided, convert it to its enum value and update the parameters.
        if role:
            try:
                role_id = UserRole[role.upper()].value
                params["role_id"] = role_id
                del params["role"]
            except KeyError:
                return "You've specified an invalid role, please double check the parameters and try again", 422

        # Attempt to update the user's information.
        try:
            user.update(update_params=params)
            message = "User successfully updated"
            status_code = 200
        except ValueError:
            pass

        return message, status_code

    # Define a method to log a user in.
    def login(
        self, username: str, password: str
    ) -> tuple[Literal["Successfully logged-in"], Literal[200]] | tuple[str, Literal[422]]:
        # Fetch the user using the given username.
        user = User.find_by(username=username)

        # Check if user exists and the password matches.
        if user:
            user_password = password.encode("utf-8")
            if bcrypt.checkpw(user_password, user.password.encode("utf-8")):
                # Store the user auth token in a file (not recommended for production systems).
                with open(f"{HERE}/../../../.auth", "w") as file:
                    file.write(user.auth_token)
                return "Successfully logged-in", 200

        # Return an error if login fails.
        return "An error occurred while trying to log-in, please double check your credentials and try again.", 422

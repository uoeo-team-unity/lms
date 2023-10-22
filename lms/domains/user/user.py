# Import necessary modules and types
import os

from typing import Final, Literal

# Import relevant components from Flask
from flask import Blueprint, Response, jsonify, request

# Import authorisation decorators from the lms.common module
from lms.common import authorise_admin, authorise_admin_or_teacher

# Import User model and UserRole enumeration
from .user_model import User, UserRole

# Import UserService for user-related operations
from .user_service import UserService

# Define a constant for the directory where this script is located
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

# Create a Blueprint object to organise a group of related views and other code
user_domain = Blueprint("user_domain", __name__, url_prefix="/users")


# Define a route to create a new user, accessible only by admin users
@user_domain.post("/create")
@authorise_admin
def create_user() -> tuple[Response, Literal[422] | Literal[201]]:
    # Retrieve user data from the request's JSON payload
    user_data = request.get_json()
    # Call the create method from UserService to handle the creation of the user
    message, status = UserService().create(params=user_data)

    # Return a JSON response with the appropriate message and status code
    return jsonify({"message": message}), status


# Define a route to list all users, accessible by admin users and teachers
@user_domain.get("/list")
@authorise_admin_or_teacher
def get_all_users() -> tuple[Response, Literal[200]]:
    # Retrieve all user records from the database
    users = User.query.all()

    # Construct a list of users with specific attributes to be returned
    users = [
        {
            "id": user.id,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "username": user.username,
            "role_id": user.role_id,
        }
        for user in users
    ]

    # Return the list of users as a JSON response with a 200 OK status
    return jsonify(users), 200


# Define a route to get details of a specific user, accessible only by admin users
@user_domain.get("/<int:user_id>")
@authorise_admin
def get_user(user_id) -> tuple[Response, Literal[200]] | tuple[Response, Literal[422]]:
    # Retrieve a user by their ID
    user = User.get(user_id)

    # Check if the user exists
    if user:
        # Return the user's details as a JSON response with a 200 OK status
        return (
            jsonify(
                {
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "username": user.username,
                    "role_id": user.role_id,
                }
            ),
            200,
        )

    # If the user does not exist, return an error message with a 422 Unprocessable Entity status
    return jsonify({"message": "No user found, please try again"}), 422


# Define a route to update user details, accessible only by admin users
@user_domain.put("/<int:user_id>")
@authorise_admin
def update_user(user_id) -> tuple[Response, Literal[422, 200]]:
    # Retrieve user data from the request's JSON payload
    user_data = request.get_json()
    # Call the update method from UserService to handle updating the user's details
    message, status = UserService().update(user_id=user_id, params=user_data)

    # Return a JSON response with the appropriate message and status code
    return jsonify({"message": message}), status


# Define a route to list all students, accessible by admin users and teachers
@user_domain.get("/list_students")
@authorise_admin_or_teacher
def list_all_students() -> tuple[Response, Literal[200]]:
    # Retrieve all user records where the role is 'STUDENT'
    students = User.query.where(User.role_id == UserRole.STUDENT.value).all()

    # Construct a list of students with specific attributes to be returned
    students = [
        {
            "id": student.id,
            "first_name": student.first_name,
            "last_name": student.last_name,
        }
        for student in students
    ]

    # Return the list of students as a JSON response with a 200 OK status
    return jsonify(students), 200

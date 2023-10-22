# Import necessary libraries
import os

from typing import Final, Literal

from flask import Response, jsonify, request
from werkzeug.exceptions import BadRequest

# Importing domain-specific modules to be used as blueprints in the Flask application
from lms.domains import UserService, assignment_domain, feature_switch_domain, grade_domain, module_domain, user_domain
from lms.make_app import make_app

# Define constants for file paths
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))  # The directory of this script
AUTH_TOKEN_PATH = f"{HERE}/../.auth"  # The path to the authentication token file

# Initialise the Flask application
app = make_app()

# Registering blueprints (domain modules) with the Flask application
for domain in (
    assignment_domain,
    feature_switch_domain,
    grade_domain,
    module_domain,
    user_domain,
):
    app.register_blueprint(domain)


# Define the route for the root endpoint
@app.get("/")
def root() -> Response:
    """Handle requests to the root endpoint."""
    # Return a JSON response indicating that the service is up and running
    return jsonify({"message": "hi!", "status": "up"})


# Define the route for the login endpoint
@app.post("/login")
def login() -> Response:
    """Handle login requests."""
    # Attempt to parse the JSON data from the request
    login_data = request.get_json()

    # If login data is provided, attempt to log in
    if login_data:
        username = login_data.get("username")
        password = login_data.get("password")

        # Authenticate the user and obtain a response message and status code
        message, status = UserService().login(username=username, password=password)

        # Return a JSON response with the authentication result
        return jsonify({"message": message}), status

    # If login data is not provided, return a bad request response
    return jsonify({"message": "Bad request"}), 400


# Define the route for the logout endpoint
@app.put("/logout")
def logout() -> tuple[Response, Literal[200]]:
    """Handle logout requests."""
    # If the authentication token file exists, remove it to log out
    if os.path.exists(AUTH_TOKEN_PATH):
        os.remove(AUTH_TOKEN_PATH)

    # Return a JSON response indicating a successful logout
    return jsonify({"message": "Successfully logged-out of the app"}), 200

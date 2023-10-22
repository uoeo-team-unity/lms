# Import necessary modules and functions from standard libraries and Flask framework
import os

from typing import Final, Literal

from flask import Blueprint, Response, jsonify, request

# Import the authorise_teacher decorator from the lms.decorators module
from lms.decorators import authorise_teacher

# Import Assignment model and AssignmentService from the current package
from .assignment_model import Assignment
from .assignment_service import AssignmentService

# Define a constant to hold the directory path of this script
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

# Create a Flask Blueprint to group and organise a set of related views and other code
assignment_domain = Blueprint("assignment_domain", __name__, url_prefix="/assignments")


# Define a route to create a new assignment, and protect it with the authorise_teacher decorator
@assignment_domain.post("/create")
@authorise_teacher
def create_assignment(current_user) -> tuple[Response, Literal[422] | Literal[201]]:
    # Parse JSON data from the request body
    data = request.get_json()
    # Call the create method from AssignmentService to handle assignment creation
    message, status = AssignmentService().create(current_user=current_user, params=data)

    # Return a JSON response with the status message and HTTP status code
    return jsonify({"message": message}), status


# Define a route to list all available assignments, and protect it with the authorise_teacher decorator
@assignment_domain.get("/list")
@authorise_teacher
def list_available_assignment(current_user) -> tuple[Response, Literal[200]]:
    # Query the database to fetch all assignment records
    assignments = Assignment.query.all()

    # Build a list of dictionaries, each representing an assignment with specific attributes
    assignments = [
        {
            "id": assignment.id,
            "title": assignment.title,
        }
        for assignment in assignments
    ]

    # Return the list of assignments as a JSON response with a 200 OK status
    return jsonify(assignments), 200

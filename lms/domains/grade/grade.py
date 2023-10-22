# Import necessary modules and classes
import os

from typing import Final

from flask import Blueprint, Response, jsonify, request

# Import custom decorators for authorisation
from lms.decorators import authorise_teacher, authorise_user

# Import the GradeService class from the current package
from .grade_service import GradeService

# Define a constant to hold the directory path of this script
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

# Create a Flask Blueprint to group and organise related views
grade_domain = Blueprint("grade_domain", __name__, url_prefix="/grades")


# Define a route to create a new grade and protect it with the authorise_teacher decorator
@grade_domain.post("/create")
@authorise_teacher
def create_grade(current_user) -> tuple[Response, int]:
    """
    Handle the creation of a new grade.
    """
    # Parse JSON data from the request body
    data = request.get_json()
    # Call the create method from GradeService to handle the grade creation
    message, status = GradeService().create(params=data)

    # Return a JSON response with the appropriate message and status code
    return jsonify({"message": message}), status


# Define a route to view all grades for a student and protect it with the authorise_user decorator
@grade_domain.get("/view")
@authorise_user
def view_grades(current_user) -> tuple[Response, int]:
    """
    Handle the retrieval of all grades for a student.
    """
    # Check if the current user is a student
    if not current_user.is_student():
        # Return an error message and a 422 Unprocessable Entity status code if the user is not a student
        return jsonify({"message": "You are not a student, so there are no grades to view"}), 422

    # Return the student's grades as a JSON response with a 200 OK status code
    return jsonify(current_user.grades), 200

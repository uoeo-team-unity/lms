# Import necessary modules and classes
import os

from typing import Final, Literal

from flask import Blueprint, Response, jsonify, request

# Import custom decorator for authorisation
from lms.decorators import authorise_teacher

# Import the Module model and ModuleService from the current package
from .module_model import Module
from .module_service import ModuleService

# Define a constant to hold the directory path of this script
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))

# Create a Flask Blueprint to group and organise related views
module_domain = Blueprint("module_domain", __name__, url_prefix="/modules")


# Define a route to create a new module and protect it with the authorise_teacher decorator
@module_domain.post("/create")
@authorise_teacher
def create_module(current_user) -> tuple[Response, Literal[422] | Literal[201]]:
    """
    Handle the creation of a new module.
    """
    # Parse JSON data from the request body
    user_data = request.get_json()
    # Call the create method from ModuleService to handle the module creation
    message, status = ModuleService().create(current_user=current_user, params=user_data)

    # Return a JSON response with the appropriate message and status code
    return jsonify({"message": message}), status


# Define a route to list all available modules and protect it with the authorise_teacher decorator
@module_domain.get("/list")
@authorise_teacher
def list_available_modules(current_user) -> tuple[Response, Literal[200]]:
    """
    Handle the retrieval of all available modules.
    """
    # Fetch all module records from the database
    modules = Module.query.all()

    # Construct a list of modules with specific attributes to be returned
    modules = [
        {
            "id": module.id,
            "title": module.title,
        }
        for module in modules
    ]
    # Return the list of modules as a JSON response with a 200 OK status
    return jsonify(modules), 200

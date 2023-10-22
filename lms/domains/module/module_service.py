# Import required modules and types
import os

from typing import Final, Literal

# Import the Module model from the current package
from .module_model import Module

# Define a constant for the directory where this script is located
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


# Define a service class for handling module-related operations
class ModuleService:
    def create(self, current_user, params: dict[str, str | int]) -> tuple[str, Literal[422] | Literal[201]]:
        # Attempt to retrieve module attributes from the provided parameters
        title = params.get("title")
        description = params.get("description")

        # Initialise a variable to hold the teacher's ID
        teacher_id = None

        # Attempt to retrieve the teacher's ID from the current user
        try:
            teacher_id = current_user.id
        except AttributeError:
            pass  # If unsuccessful, teacher_id remains None

        # Validate that all required parameters are present
        if not all([title, description, teacher_id]):
            # If any are missing, return an error message and a 422 Unprocessable Entity status
            return "Something doesn't look right, please double-check the parameters and try again", 422

        # Create a new module with the provided attributes
        Module.create(title=title, description=description, teacher_id=teacher_id)

        # Return a success message and a 201 Created status
        return f"Module with title {title} successfully created", 201

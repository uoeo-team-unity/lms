# Import the Assignment model from assignment_model module.
from .assignment_model import Assignment


# Define a class to handle assignment-related services.
class AssignmentService:
    # Define a method to create a new assignment.
    def create(self, current_user, params: dict[str, str | int | float]) -> tuple[str, int]:
        # Extract assignment details from parameters.
        title = params.get("title")
        description = params.get("description")
        module_id = params.get("module_id")
        due_date = params.get("due_date")

        # Check if all required parameters are present.
        if not all([title, description, module_id, due_date]):
            # Return an error message and a 422 Unprocessable Entity status code if any parameter is missing.
            return "Something doesn't look right, please double-check the parameters and try again", 422

        # Use the Assignment model's create class method to save the new assignment to the database.
        Assignment.create(title=title, description=description, module_id=module_id, due_date=due_date)

        # Return a success message and a 201 Created status code.
        return f"Assignment with title {title} successfully created", 201

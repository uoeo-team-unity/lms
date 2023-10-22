# Import the Grade model from the grade_model module within the current package
from .grade_model import Grade


# Define a service class to handle operations related to grades
class GradeService:
    # Define a method to create a new grade entry
    def create(self, params: dict[str, int | float]) -> tuple[str, int]:
        # Extract student ID, assignment ID, and score from the provided parameters
        student_id = params.get("student_id")
        assignment_id = params.get("assignment_id")
        score = params.get("score")

        # Check if all required parameters are present
        if not all([student_id, assignment_id, score]):
            # Return an error message and a 422 status code if any parameter is missing
            return "Something doesn't look right, please double-check the parameters and try again", 422

        # Create a new grade entry in the database
        Grade.create(student_id=student_id, assignment_id=assignment_id, score=score)

        # Return a success message and a 201 status code
        return f"Grade for student {student_id} and assignment {assignment_id} successfully created", 201

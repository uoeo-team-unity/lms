import secrets

from typing import TYPE_CHECKING

from lms.app import app
from tests.factories import AssignmentFactory, GradeFactory, ModuleFactory, StudentFactory, TeacherFactory, UserFactory

# Conditional import for type checking
if TYPE_CHECKING:
    from lms.domains import Assignment, User


# Function to create an admin user
def create_admin_user() -> "User":
    """
    Create a default admin user for the LMS.
    Returns the created admin user object.
    """
    # Define admin user credentials
    admin_user = "admin"
    admin_password = "$2b$12$6I5Ls.Z7UNfYZZHV.ElhJ.qu/.g/2CW3W9VzQPpP.7YdgxYman.2S"

    # Create the admin user using the UserFactory
    admin = UserFactory.create(
        username=admin_user,
        first_name=admin_user,
        last_name=admin_user,
        password=admin_password,
        email="admin@admin.com",
        auth_token=secrets.token_hex(24),  # Generate a random authentication token
    )
    return admin


# Function to create a teacher user
def create_teacher_user() -> "User":
    """
    Create a default teacher user for the LMS.
    Returns the created teacher user object.
    """
    # Define teacher user credentials
    teacher_user = "teacher"
    teacher_password = "$2b$12$hHg0grc8eHimaZmoB42IReoAio8sA/GdymEVcgha/EIrucPKkGk/S"

    # Create the teacher user using the TeacherFactory
    teacher = TeacherFactory.create(
        username=teacher_user,
        first_name=teacher_user,
        last_name=teacher_user,
        password=teacher_password,
        email="teacher@teacher.com",
        auth_token=secrets.token_hex(24),  # Generate a random authentication token
    )
    return teacher


# Function to create a student user
def create_student_user() -> "User":
    """
    Create a default student user for the LMS.
    Returns the created student user object.
    """
    # Define student user credentials
    student_user = "student"
    student_password = "$2b$12$Lin26rHVfL8anWmBFwovdO54CiyAr6Let8ZD/m0PbQNHO24ScG6EK"

    # Create the student user using the StudentFactory
    student = StudentFactory.create(
        username=student_user,
        first_name=student_user,
        last_name=student_user,
        password=student_password,
        email="student@student.com",
        auth_token=secrets.token_hex(24),  # Generate a random authentication token
    )
    return student


# Function to create an assignment
def create_assignment(teacher_id: int, student_id: int) -> "Assignment":
    """
    Create a default assignment in a module.
    Returns the created assignment object.
    """
    # Create a module using the ModuleFactory and associate it with the teacher
    module = ModuleFactory.create(teacher_id=teacher_id)

    # Create an assignment using the AssignmentFactory and associate it with the module
    assignment = AssignmentFactory.create(module_id=module.id)
    return assignment


# Function to create a grade for an assignment
def create_grade(assignment_id: int, student_id: int) -> None:
    """
    Create a default grade for an assignment.
    """
    # Create a grade using the GradeFactory and associate it with the assignment and student
    GradeFactory.create(assignment_id=assignment_id, student_id=student_id)


# Function to seed initial data into the LMS system
def seed_data() -> None:
    """
    Seed the database with initial data for testing.
    """
    # Ensure we are running in the Flask app context
    with app.app_context():
        # Create default users and assignments
        create_admin_user()
        teacher = create_teacher_user()
        student = create_student_user()
        assignment = create_assignment(teacher_id=teacher.id, student_id=student.id)
        create_grade(assignment_id=assignment.id, student_id=student.id)

        # Create a default grade with random data
        GradeFactory.create()


# Main entry point for the script
if __name__ == "__main__":
    seed_data()

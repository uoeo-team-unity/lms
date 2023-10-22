import factory

from lms.domains import Grade

from .assignment_factory import AssignmentFactory
from .base import BaseFactory
from .user_factory import StudentFactory

# Create a factory for generating Grade instances.
class GradeFactory(BaseFactory):
    class Meta:
        model = Grade
        exclude = ["student", "assignment"]

    # Generate a random score using the Faker library, between 0 and 100.
    score = factory.Faker("pyint", min_value=0, max_value=100)

    # Create a sub-factory for generating a Student instance associated with the grade.
    student = factory.SubFactory(StudentFactory)

    # Set the student_id attribute to the id of the associated student using SelfAttribute.
    student_id = factory.SelfAttribute("student.id")

    # Create a sub-factory for generating an Assignment instance associated with the grade.
    assignment = factory.SubFactory(AssignmentFactory)

    # Set the assignment_id attribute to the id of the associated assignment using SelfAttribute.
    assignment_id = factory.SelfAttribute("assignment.id")

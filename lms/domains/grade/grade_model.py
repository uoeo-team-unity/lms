# Import the dataclass decorator for creating data classes
from dataclasses import dataclass

# Import necessary SQLAlchemy classes for defining the model
from sqlalchemy import Float, ForeignKey
from sqlalchemy.orm import relationship

# Import base mixin and database instance from lms.adapters
from lms.adapters import BaseMixin, db


# Define a data class to represent a grade
@dataclass
class Grade(BaseMixin, db.Model):
    # Specify the table name for this model in the database
    __tablename__ = "grades"

    # Define the columns for the Grade table
    student_id: int = db.Column(db.Integer, ForeignKey("users.id"), nullable=True)
    assignment_id: int = db.Column(db.Integer, ForeignKey("assignments.id"), nullable=True)
    score: float = db.Column(Float, nullable=False)
    assignment = relationship("Assignment", backref="grades")

    # Initialise a Grade object
    def __init__(self, score: float, student_id: int, assignment_id: int) -> None:
        self.score = score
        self.student_id = student_id
        self.assignment_id = assignment_id

    # Define a class method to create and save a grade object to the database
    @classmethod
    def create(cls, score: float, student_id: int, assignment_id: int) -> "Grade":
        # Instantiate a Grade object
        grade = cls(score=score, student_id=student_id, assignment_id=assignment_id)
        # Add the grade object to the database session
        db.session.add(grade)
        # Commit the changes to the database
        db.session.commit()
        # Return the created grade object
        return grade

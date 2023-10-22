# Import classes for data modelling and handling dates
from dataclasses import dataclass
from datetime import date

# Import SQLAlchemy functions and classes for database operations
from sqlalchemy import Date, ForeignKey, Text
from sqlalchemy.orm import relationship

# Import base mixin and database instance from lms.adapters
from lms.adapters import BaseMixin, db


# Define a data class to represent an Assignment
@dataclass
class Assignment(BaseMixin, db.Model):
    # Specify the table name for this model in the database
    __tablename__ = "assignments"

    # Define the columns for the Assignment table
    title: str = db.Column(db.String(255), nullable=False)  # Store the title, cannot be null
    description: str = db.Column(Text, nullable=True)  # Store the description, can be null
    module_id: int = db.Column(db.Integer, ForeignKey("modules.id"), nullable=True)  # Store module ID as a foreign key
    due_date: date = db.Column(Date, nullable=True)  # Store the due date, can be null

    # Establish a relationship with the Module table, creating a back reference for assignments
    module = relationship("Module", backref="assignments")

    # Initialise an Assignment object
    def __init__(self, title: str, description: str, module_id: int, due_date: date) -> None:
        self.title = title
        self.description = description
        self.module_id = module_id
        self.due_date = due_date

    # Define a class method to create and save an assignment object to the database
    @classmethod
    def create(cls, title: str, description: str, module_id: int, due_date: date) -> "Assignment":
        # Instantiate an Assignment object
        assignment = cls(title=title, description=description, module_id=module_id, due_date=due_date)
        # Add the assignment object to the database session
        db.session.add(assignment)
        # Commit the changes to the database
        db.session.commit()
        # Return the created assignment object
        return assignment

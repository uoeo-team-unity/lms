# Import the dataclass decorator to facilitate the creation of data classes
from dataclasses import dataclass

# Import necessary components from SQLAlchemy for database interaction
from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import relationship

# Import the base mixin and database instance from the lms.adapters module
from lms.adapters import BaseMixin, db


# Define a data class to represent a Module in the database
@dataclass
class Module(BaseMixin, db.Model):
    # Specify the table name in the database for this model
    __tablename__ = "modules"

    # Define the columns for the Module table
    # Store the title of the module, must not be null
    title: str = db.Column(db.String(255), nullable=False)
    # Store a description of the module, can be null
    description: str = db.Column(Text, nullable=True)
    # Store the teacher's ID, creating a foreign key relationship
    teacher_id: int = db.Column(db.Integer, ForeignKey("users.id"), nullable=True)

    # Create a relationship with the User table, establishing a back reference for modules
    teacher = relationship("User", backref="modules")

    # Initialise the Module object with the provided attributes
    def __init__(self, title: str, description: str, teacher_id: int) -> None:
        self.title = title
        self.description = description
        self.teacher_id = teacher_id

    # Offer a class method to create a new Module instance and save it to the database
    @classmethod
    def create(cls, title: str, description: str, teacher_id: int) -> "Module":
        # Instantiate a Module
        module = cls(title=title, description=description, teacher_id=teacher_id)
        # Add the module to the current database session
        db.session.add(module)
        # Commit the transaction to the database
        db.session.commit()
        # Return the created module
        return module

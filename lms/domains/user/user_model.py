import enum

# Import the necessary libraries and modules
from dataclasses import dataclass

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import relationship

from lms.adapters import BaseMixin, db


# Define the UserRole enumeration for managing user roles
class UserRole(enum.Enum):
    ADMIN = 1
    TEACHER = 2
    STUDENT = 3


# Utilise the dataclass decorator to automatically generate special methods
@dataclass
class User(BaseMixin, db.Model):
    # Set the table name for the User model
    __tablename__ = "users"

    # Define the User model attributes with their respective data types and constraints
    username: str = db.Column(db.String, unique=True, nullable=False)
    password: str = db.Column(db.String, nullable=False)
    role_id: int = db.Column(db.Integer, nullable=False)
    first_name: str = db.Column(db.String, nullable=False)
    last_name: str = db.Column(db.String, nullable=False)
    email: str = db.Column(db.String, unique=True, nullable=False)
    auth_token: str = db.Column(db.String(255), unique=True)

    # Establish a relationship with the Grade model
    grades = relationship("Grade", backref="users")

    # Define the constructor for initialising User objects
    def __init__(
        self,
        username: str,
        password: str,
        role_id: int,
        first_name: str,
        last_name: str,
        email: str,
        auth_token: str,
    ) -> None:
        self.username = username
        self.password = password
        self.role_id = role_id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.auth_token = auth_token

    # Define a class method to create and return a new User object
    @classmethod
    def create(
        cls, username: str, password: str, role_id: int, first_name: str, last_name: str, email: str, auth_token: str
    ) -> "User":
        user = cls(
            username=username,
            password=password,
            role_id=role_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            auth_token=auth_token,
        )
        db.session.add(user)
        db.session.commit()
        return user

    # Define a method to update user attributes and save changes to the database
    def update(self, update_params: dict) -> "User":
        self.username = update_params.get("username", self.username)
        self.role_id = update_params.get("role_id", self.role_id)
        self.first_name = update_params.get("first_name", self.first_name)
        self.last_name = update_params.get("last_name", self.last_name)
        self.email = update_params.get("email", self.email)

        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()
            raise ValueError("Invalid params")

        return self

    # Define methods to check the user's role
    def is_admin(self) -> bool:
        return self.role_id == UserRole.ADMIN.value

    def is_teacher(self) -> bool:
        return self.role_id == UserRole.TEACHER.value

    def is_student(self) -> bool:
        return self.role_id == UserRole.STUDENT.value

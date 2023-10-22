import factory

from lms.domains import User, UserRole

from .base import BaseFactory

# Create a factory for generating User instances.
class UserFactory(BaseFactory):
    class Meta:
        model = User

    # Generate a random username using the Faker library.
    username = factory.Faker("name")

    # Generate a random first name using the Faker library.
    first_name = factory.Faker("first_name")

    # Generate a random last name using the Faker library.
    last_name = factory.Faker("last_name")

    # Generate a random email address using the Faker library.
    email = factory.Faker("email")

    # Generate a random password using the Faker library.
    password = factory.Faker("password")

    # Set the role_id to UserRole.ADMIN's value.
    role_id = UserRole.ADMIN.value

    # Generate a random authentication token using the Faker library.
    auth_token = factory.Faker("password")

# Create a factory for generating Teacher instances.
class TeacherFactory(BaseFactory):
    class Meta:
        model = User

    # Generate a random username using the Faker library.
    username = factory.Faker("name")

    # Generate a random first name using the Faker library.
    first_name = factory.Faker("first_name")

    # Generate a random last name using the Faker library.
    last_name = factory.Faker("last_name")

    # Generate a random email address using the Faker library.
    email = factory.Faker("email")

    # Generate a random password using the Faker library.
    password = factory.Faker("password")

    # Set the role_id to UserRole.TEACHER's value.
    role_id = UserRole.TEACHER.value

    # Generate a random authentication token using the Faker library.
    auth_token = factory.Faker("password")

# Create a factory for generating Student instances.
class StudentFactory(BaseFactory):
    class Meta:
        model = User

    # Generate a random username using the Faker library.
    username = factory.Faker("name")

    # Generate a random first name using the Faker library.
    first_name = factory.Faker("first_name")

    # Generate a random last name using the Faker library.
    last_name = factory.Faker("last_name")

    # Generate a random email address using the Faker library.
    email = factory.Faker("email")

    # Generate a random password using the Faker library.
    password = factory.Faker("password")

    # Set the role_id to UserRole.STUDENT's value.
    role_id = UserRole.STUDENT.value

    # Generate a random authentication token using the Faker library.
    auth_token = factory.Faker("password")

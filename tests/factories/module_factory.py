import factory

from lms.domains import Module

from .base import BaseFactory
from .user_factory import TeacherFactory

# Create a factory for generating Module instances.
class ModuleFactory(BaseFactory):
    class Meta:
        model = Module
        exclude = ["teacher"]

    # Generate a random title using the Faker library with 4 words.
    title = factory.Faker("sentence", nb_words=4)

    # Generate a random description using the Faker library for the module.
    description = factory.Faker("paragraph")

    # Create a sub-factory for generating a Teacher instance associated with the module.
    teacher = factory.SubFactory(TeacherFactory)

    # Set the teacher_id attribute to the id of the associated teacher using SelfAttribute.
    teacher_id = factory.SelfAttribute("teacher.id")

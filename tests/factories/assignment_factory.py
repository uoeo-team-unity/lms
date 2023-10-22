import factory

from lms.domains import Assignment

# Import the base factory class.
from .base import BaseFactory
# Import the ModuleFactory for creating associated modules.
from .module_factory import ModuleFactory

# Define the AssignmentFactory class that inherits from the BaseFactory.
class AssignmentFactory(BaseFactory):
    class Meta:
        model = Assignment  # Specify the model to use for creating Assignment objects.
        exclude = ["module"]  # Exclude the "module" field when creating an Assignment object.

    # Generate a random title for the assignment.
    title = factory.Faker("sentence", nb_words=4)
    # Generate a random paragraph for the assignment description.
    description = factory.Faker("paragraph")
    # Create an associated Module for the assignment using ModuleFactory.
    module = factory.SubFactory(ModuleFactory)
    # Set the module_id to the ID of the associated module.
    module_id = factory.SelfAttribute("module.id")
    # Generate a random future due date for the assignment.
    due_date = factory.Faker("future_date")

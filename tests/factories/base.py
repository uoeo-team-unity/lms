import factory

from lms.adapters import db


# Create a base factory class that inherits from SQLAlchemyModelFactory.
class BaseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        # Indicate that this is an abstract factory and is not used directly.
        abstract = True
        # Use the SQLAlchemy session provided by the db adapter.
        sqlalchemy_session = db.session
        # Specify that objects created by the factory should be persisted to the database through a commit operation.
        sqlalchemy_session_persistence = "commit"

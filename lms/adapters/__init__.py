# Importing BaseMixin and db from the database module
from .database import BaseMixin, db

# Defining the public interface of the package.
# This allows other modules to access BaseMixin and db when they import this package.
__all__ = ["BaseMixin", "db"]

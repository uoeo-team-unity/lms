# Import necessary standard library and third-party modules
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer

# Initialise an instance of SQLAlchemy for ORM-based interactions with the database
db = SQLAlchemy()


# Define a mixin class to provide common fields and methods for database models
@dataclass
class BaseMixin(object):
    # Define common fields for database models
    id = db.Column(Integer, primary_key=True, autoincrement=True)  # Unique identifier for each record
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)  # Timestamp of record creation
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)  # Timestamp of last update

    # Define a class method to retrieve a record by its unique identifier
    @classmethod
    def get(cls, id) -> Any:
        return cls.query.get(id)

    # Define a class method to retrieve the first record matching the provided filter criteria
    @classmethod
    def find_by(cls, **kwargs) -> Any | None:
        filters = cls._filters(kwargs)  # Generate filter conditions based on provided keyword arguments
        return db.session.execute(db.select(cls).where(*filters)).scalars().first()

    # Define a class method to generate filter conditions for SQLAlchemy queries
    @classmethod
    def _filters(cls, kwargs) -> list[Any]:
        return [getattr(cls, attr) == kwargs[attr] for attr in kwargs]

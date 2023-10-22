# Import the dataclass decorator for creating data classes
from dataclasses import dataclass

# Import base mixin and database instance from lms.adapters
from lms.adapters import BaseMixin, db


# Define a data class to represent a feature switch
@dataclass
class FeatureSwitch(BaseMixin, db.Model):
    # Specify the table name for this model in the database
    __tablename__ = "feature_switches"

    # Define the columns for the feature switch table
    name: str = db.Column("name", db.String(255), nullable=False)  # Store the name, cannot be null
    active: int = db.Column("active", db.Integer, nullable=False, default=0)  # Store the active status, cannot be null

    # Initialise a FeatureSwitch object
    def __init__(self, name: str, active: int = 0) -> None:
        self.name = name
        self.active = active

    # Define a class method to create and save a feature switch object to the database
    @classmethod
    def create(cls, name: str, active: int = 0) -> "FeatureSwitch":
        # Instantiate a FeatureSwitch object
        feature_switch = cls(name=name, active=active)
        # Add the feature switch object to the database session
        db.session.add(feature_switch)
        # Commit the changes to the database
        db.session.commit()
        # Return the created feature switch object
        return feature_switch

    # Define a method to update the active status of the feature switch and save changes to the database
    def set_value(self, active: int) -> None:
        self.active = active
        db.session.commit()

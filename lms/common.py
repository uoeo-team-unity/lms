import os

from functools import wraps
from typing import Any, Final

from lms.domains.feature_switch import FeatureSwitch
from lms.domains.user.user_model import User

# Define a constant for the directory where this script is located
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


# Decorator to authorise admin users
def authorise_admin(function) -> Any:
    """
    A decorator to authorise admin users.
    """

    @wraps(function)
    def check_user_auth(*args, **kwargs) -> Any:
        # Fetch the hacker_mode feature switch status from the database
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If the hacker mode is active, bypass the authorisation and impersonate the current user
        if hacker_mode and hacker_mode.active:
            return function(*args, **kwargs)

        access_token = None

        # Attempt to read the access token from a file
        try:
            with open(f"{HERE}/../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        # Find the current user based on the access token
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If the user is not an admin, return an error message and a 401 status code
        if not current_user.is_admin():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed with the original function
        return function(*args, **kwargs)

    return check_user_auth


# Decorator to authorise admin or teacher users
def authorise_admin_or_teacher(function) -> Any:
    """
    A decorator to authorise admin or teacher users.
    """

    @wraps(function)
    def check_admin_or_teacher_auth(*args, **kwargs) -> Any:
        # Fetch the hacker_mode feature switch status from the database
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If the hacker mode is active, bypass the authorisation and impersonate the current user
        if hacker_mode and hacker_mode.active:
            return function(*args, **kwargs)

        access_token = None

        # Attempt to read the access token from a file
        try:
            with open(f"{HERE}/../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        # Find the current user based on the access token
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If the user is a student, return an error message and a 401 status code
        if current_user.is_student():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed with the original function
        return function(*args, **kwargs)

    return check_admin_or_teacher_auth

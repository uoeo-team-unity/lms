import os

from functools import wraps
from typing import Any, Final

from lms.domains.feature_switch import FeatureSwitch
from lms.domains.user.user_model import User

# Define a constant for the directory where this script is located.
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


def authorise_teacher(function) -> Any:
    """
    A decorator to authorise teacher users.
    """

    @wraps(function)
    def check_teacher_auth(*args, **kwargs) -> Any:
        # Fetch the 'hacker_mode' feature switch status from the database.
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If 'hacker_mode' is active, bypass the authorisation check.
        if hacker_mode and hacker_mode.active:
            current_user = User.find_by(username="teacher")
            return function(*args, **kwargs, current_user=current_user)

        # Initialise the access token variable.
        access_token = None

        try:
            # Try to read the access token from the .auth file located two directories up from this script.
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            # If the file is not found, continue with a None access token.
            pass

        # Fetch the user associated with the access token from the database.
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code.
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If the user is not a teacher, return an error message and a 401 status code.
        if not current_user.is_teacher():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed to the original function.
        return function(*args, **kwargs, current_user=current_user)

    return check_teacher_auth


def authorise_student(function) -> Any:
    """
    A decorator to authorise student users.
    """

    @wraps(function)
    def check_student_auth(*args, **kwargs) -> Any:
        # Fetch the 'hacker_mode' feature switch status from the database.
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If 'hacker_mode' is active, bypass the authorisation check.
        if hacker_mode and hacker_mode.active:
            current_user = User.find_by(username="admin")
            return function(*args, **kwargs, current_user=current_user)

        # Initialise the access token variable.
        access_token = None

        try:
            # Try to read the access token from the .auth file located two directories up from this script.
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            # If the file is not found, continue with a None access token.
            pass

        # Fetch the user associated with the access token from the database.
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code.
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If the user is not a student, return an error message and a 401 status code.
        if not current_user.is_student():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed to the original function.
        return function(*args, **kwargs, current_user=current_user)

    return check_student_auth


def authorise_user(function) -> Any:
    """
    A decorator to authorise any authenticated user.
    """

    @wraps(function)
    def check_student_or_teacher_auth(*args, **kwargs) -> Any:
        # Fetch the 'hacker_mode' feature switch status from the database.
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If 'hacker_mode' is active, bypass the authorisation check.
        if hacker_mode and hacker_mode.active:
            current_user = User.find_by(username="teacher")
            return function(*args, **kwargs, current_user=current_user)

        # Initialise the access token variable.
        access_token = None

        try:
            # Try to read the access token from the .auth file located two directories up from this script.
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            # If the file is not found, continue with a None access token.
            pass

        # Fetch the user associated with the access token from the database.
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code.
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed to the original function.
        return function(*args, **kwargs, current_user=current_user)

    return check_student_or_teacher_auth


def authorise_teacher_or_admin(function) -> Any:
    """
    A decorator to authorise teacher or admin users.
    """

    @wraps(function)
    def check_teacher_or_admin_auth(*args, **kwargs) -> Any:
        # Fetch the 'hacker_mode' feature switch status from the database.
        hacker_mode = FeatureSwitch.find_by(name="hacker_mode")
        # If 'hacker_mode' is active, bypass the authorisation check.
        if hacker_mode and hacker_mode.active:
            current_user = User.find_by(username="admin")
            return function(*args, **kwargs, current_user=current_user)

        # Initialise the access token variable.
        access_token = None

        try:
            # Try to read the access token from the .auth file located two directories up from this script.
            with open(f"{HERE}/../../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            # If the file is not found, continue with a None access token.
            pass

        # Fetch the user associated with the access token from the database.
        current_user = User.find_by(auth_token=access_token)

        # If no user is found, return an error message and a 401 status code.
        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorisation and try again."
            }, 401

        # If all checks pass, proceed to the original function.
        return function(*args, **kwargs, current_user=current_user)

    return check_teacher_or_admin_auth

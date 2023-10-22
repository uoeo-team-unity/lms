import os

from functools import wraps
from typing import Any, Final

from lms.domains.user.user_model import User

HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


def authorise_admin(function) -> Any:
    @wraps(function)
    def check_user_auth(*args, **kwargs) -> Any:
        access_token = None

        try:
            with open(f"{HERE}/../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        current_user = User.find_by(auth_token=access_token)

        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorization and try again."
            }, 401

        if not current_user.is_admin():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            }, 401

        return function(*args, **kwargs)

    return check_user_auth


def authorise_admin_or_teacher(function) -> Any:
    @wraps(function)
    def check_admin_or_teacher_auth(*args, **kwargs) -> Any:
        access_token = None

        try:
            with open(f"{HERE}/../.auth", "r") as file:
                access_token = file.read().strip()
        except FileNotFoundError:
            pass

        current_user = User.find_by(auth_token=access_token)

        if not current_user:
            return {
                "message": "It appears you provided an invalid token. "
                "Please double-check your authorization and try again."
            }, 401

        if current_user.is_student():
            return {
                "message": "It appears you are not authorised to perform this action. "
                "Please double-check your authorization and try again."
            }, 401

        return function(*args, **kwargs)

    return check_admin_or_teacher_auth

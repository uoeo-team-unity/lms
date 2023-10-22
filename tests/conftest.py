import os

from typing import Generator

import pytest

from flask import Flask
from sqlalchemy import text

from lms.adapters import db as _db
from lms.app import app as _app
from lms.common import HERE
from lms.domains import FeatureSwitch
from tests.factories import StudentFactory, TeacherFactory, UserFactory

# Define the path to the authentication token file.
AUTH_TOKEN_PATH = f"{HERE}/../.auth"

# Create a fixture for the Flask application.
@pytest.fixture
def app(request) -> Generator:
    app = _app
    with app.app_context():
        yield app

# Create a fixture for the Flask test client.
@pytest.fixture()
def client(app) -> Flask:
    return app.test_client()

# Create a fixture for the database.
@pytest.fixture
def db(app, request, monkeypatch) -> Generator:
    # Connect to the database and begin a transaction.
    connection = _db.engine.connect()
    transaction = connection.begin()

    # Monkeypatch the get_engine function to return the open connection.
    monkeypatch.setattr(_db, "get_engine", lambda *args, **kwargs: connection)

    try:
        yield _db
    finally:
        _db.session.remove()
        transaction.rollback()
        connection.close()

# Create a fixture for wiping the users table.
@pytest.fixture
def wipe_users_table(db) -> Generator:
    # Wipe the users table before the test.
    db.session.execute(text("TRUNCATE users CASCADE;"))
    db.session.commit()
    yield
    # Wipe the users table after the test.
    db.session.execute(text("TRUNCATE users CASCADE;"))
    db.session.commit()

# Create a fixture for wiping the modules table.
@pytest.fixture
def wipe_modules_table(db) -> Generator:
    yield
    db.session.execute(text("TRUNCATE modules CASCADE;"))
    db.session.commit()

# Create a fixture for wiping the assignments table.
@pytest.fixture
def wipe_assignments_table(db) -> Generator:
    yield
    db.session.execute(text("TRUNCATE assignments CASCADE;"))
    db.session.commit()

# Create a fixture for wiping the grades table.
@pytest.fixture
def wipe_grades_table(db) -> Generator:
    yield
    db.session.execute(text("TRUNCATE grades CASCADE;"))
    db.session.commit()

# Create a fixture for wiping the feature_switches table.
@pytest.fixture
def wipe_feature_switch_table(db) -> Generator:
    yield
    db.session.execute(text("TRUNCATE feature_switches;"))
    db.session.commit()

# Create a fixture for the admin user.
@pytest.fixture
def admin_user(db) -> Generator:
    # Create an admin user and update the authentication token.
    admin_user = UserFactory.create()
    update_token(admin_user.auth_token)
    yield admin_user

# Create a fixture for the teacher user.
@pytest.fixture
def teacher_user(db) -> Generator:
    # Create a teacher user and update the authentication token.
    teacher_user = TeacherFactory.create()
    update_token(teacher_user.auth_token)
    yield teacher_user

# Create a fixture for the student user.
@pytest.fixture
def student_user(db) -> Generator:
    # Create a student user and update the authentication token.
    student_user = StudentFactory.create()
    update_token(student_user.auth_token)
    yield student_user

# Create a fixture for the teacher user without a token.
@pytest.fixture
def teacher_user_without_token(wipe_users_table) -> Generator:
    # Create a teacher user without an authentication token.
    teacher_user = TeacherFactory.create(username="teacher")
    yield teacher_user

# Create a fixture for toggling the "hacker_mode" feature.
@pytest.fixture
def toggle_hacker_mode(db) -> Generator:
    # Ensure the feature_switches table is clean before the test.
    db.session.execute(text("TRUNCATE feature_switches;"))
    db.session.commit()

    # Create and activate the "hacker_mode" feature switch.
    hacker_mode = FeatureSwitch.create(name="hacker_mode", active=1)
    db.session.commit()

    # Yield control to the test.
    yield

    # Deactivate the "hacker_mode" feature switch after the test.
    hacker_mode.set_value(0)
    db.session.commit()

    # Clean up the feature_switches table after the test.
    db.session.execute(text("TRUNCATE feature_switches;"))
    db.session.commit()

# Update the authentication token.
def update_token(token) -> None:
    if os.path.exists(AUTH_TOKEN_PATH):
        os.remove(AUTH_TOKEN_PATH)

    with open(AUTH_TOKEN_PATH, "w") as file:
        file.write(token)

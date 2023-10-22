# Import essential modules for operating system interactions and generating random secrets.
import os
import secrets

# Import the Final class from the typing module for type hinting.
from typing import Final

# Import the load_dotenv function to load environment variables from a .env file.
from dotenv import load_dotenv

# Import the Flask class for creating the Flask application.
from flask import Flask

# Import the Compress class for compressing responses in your Flask app.
from flask_compress import Compress

# Import CORS to handle Cross-Origin Resource Sharing.
from flask_cors import CORS

# Import the db object from the lms.adapters module.
from lms.adapters import db

# Define the path to the directory containing this script.
HERE: Final[str] = os.path.dirname(os.path.realpath(__file__))


# Define the function to create and configure the Flask application.
def make_app() -> Flask:
    # Initialise the compression object.
    compress = Compress()
    # Create the Flask application.
    app = Flask(__name__)
    # Generate and set a secret key for the application.
    app.secret_key = secrets.token_hex(24)
    # Initialise compression for the application.
    compress.init_app(app)

    # Enable and configure CORS for the application.
    CORS(app)
    # Load environment variables from a .env file.
    load_dotenv()

    # Configure session cookie security.
    app.config["SESSION_COOKIE_SECURE"] = True
    app.config["SESSION_COOKIE_HTTPONLY"] = True

    # Configure SQLAlchemy settings for the application.
    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri()
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True, "pool_recycle": 280, "pool_size": 90}

    # Initialise the database with the application.
    db.init_app(app)

    # Return the configured Flask application.
    return app


# Define the function to construct the database URI.
def database_uri() -> str:
    # Retrieve database connection details from environment variables.
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    host = os.environ.get("HOST")
    port = os.environ.get("PORT")
    database = os.environ.get("DATABASE")
    # Construct and return the database URI.
    return f"postgresql://{user}:{password}@{host}:{port}/{database}"

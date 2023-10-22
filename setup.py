from setuptools import find_packages, setup

setup(
    name="LMS",  # The name of our Python app
    version="1.0",  # The version number of our app
    author="Team Unity",  # The author
    url="https://github.com/uoeo-team-unity/lms",  # The URL to the app's source code repository
    description="LMS Application",  # The description of our app
    python_requires=">=3.11",  # The minimum Python version required to run
    packages=find_packages(),  # Automatically finds and includes all packages and sub-packages
    py_modules=["lms"],  # List of Python modules to include
)

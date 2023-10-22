"""
Team Unity - LMS application
"""
import click
import requests

# Base URL for the Learning Management System (LMS) API
API_BASE_URL = "http://localhost:5001"


# Click group to create a command-line interface
@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx) -> None:
    """
    Main function to run the LMS Command Line Interface.
    Provides a list of actions for the user to choose from.
    """

    # Display a welcome message and default admin credentials
    click.echo("If this is the first time you use this application, you can use the admin credentials")
    click.echo("username=admin, password=admin")
    click.echo("")

    # Main loop to keep the CLI running
    while True:
        # Display available actions to the user
        click.echo("Available actions:")
        click.echo("1. Login to the app")
        click.echo("2. Register a new user")
        click.echo("3. List all current users")
        click.echo("4. Update a user")
        click.echo("5. Create a Module")
        click.echo("6. Create an Assignment")
        click.echo("7. Submit a Grade")
        click.echo("8. View Grades as a Student")
        click.echo("9. Toggle Hacker Mode")
        click.echo("10. Logout")
        click.echo("11. Exit")

        # Get the user's choice
        choice = click.prompt("Please select an action", type=int)

        # Execute the corresponding function based on user's choice
        if choice == 1:
            login()
        elif choice == 2:
            register_user()
        elif choice == 3:
            list_all_users()
        elif choice == 4:
            update_user()
        elif choice == 5:
            create_module()
        elif choice == 6:
            create_assignment()
        elif choice == 7:
            submit_grade()
        elif choice == 8:
            view_grades()
        elif choice == 9:
            toggle_hacker_mode()
        elif choice == 10:
            logout()
        elif choice == 11:
            click.echo("Exiting...")
            break
        else:
            click.echo("Invalid choice. Please select again.")


# Function to register a new user
def register_user() -> None:
    """
    Registers a new user.
    Prompts the user to enter username, password, role, first name, last name, and email.
    Sends a POST request to the LMS API to create a new user.
    """
    # Get user input
    username = click.prompt("Please enter a username", type=str)
    password = click.prompt("Please enter a password", type=str, hide_input=True)
    role = click.prompt("Please enter a role (Admin, Teacher, Student)", type=str)
    first_name = click.prompt("Please enter your first name", type=str)
    last_name = click.prompt("Please enter your last name", type=str)
    email = click.prompt("Please enter your email", type=str)
    click.echo("")

    # Prepare user data
    user_data = {
        "username": username,
        "password": password,
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }

    # Send POST request to register the user
    response = requests.post(f"{API_BASE_URL}/users/create", json=user_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to log in to the system
def login() -> None:
    """
    Logs in to the LMS system.
    Prompts the user to enter username and password.
    Sends a POST request to the LMS API to log in.
    """
    # Get login credentials
    username = click.prompt("Please enter a username", type=str)
    password = click.prompt("Please enter a password", type=str, hide_input=True)
    click.echo("")

    # Prepare login data
    user_data = {"username": username, "password": password}

    # Send POST request to log in
    response = requests.post(f"{API_BASE_URL}/login", json=user_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to list all available users in the system
def list_all_users() -> None:
    """
    Lists all users in the LMS system.
    Sends a GET request to the LMS API to retrieve the list of users.
    """
    # Send GET request to retrieve user list
    response = requests.get(f"{API_BASE_URL}/users/list")
    data = response.json()

    # Check if the response is an error message
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        # Display the list of users
        start_number = 1
        click.echo("")
        click.echo("Current users in the system:")
        for user in data:
            click.echo(
                f'- User {start_number}. first name: {user.get("first_name")}, '
                f'last name: {user.get("last_name")}, username: {user.get("username")}'
            )
            start_number += 1

    click.echo("")


# Function to update an existing user
def update_user() -> None:
    """
    Updates an existing user.
    Retrieves the list of users and prompts the user to select a user to update.
    Sends a PUT request to the LMS API to update the user's details.
    """
    # Fetch the list of current users
    response = requests.get(f"{API_BASE_URL}/users/list")
    data = response.json()

    # Check if the response is an error message
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        # Display the list of users
        click.echo("")
        click.echo("Current users in the system:")
        for user in data:
            click.echo(
                f'- User ID {user.get("id")}. first name: {user.get("first_name")}, '
                f'last name: {user.get("last_name")}, username: {user.get("username")}'
            )
    click.echo("")

    # Get user input for the user to update
    user_id = click.prompt("Please enter the user ID of the user you want to update", type=int)
    username = click.prompt("Please enter a new username (or press Enter to skip)", type=str, default="")
    role = click.prompt(
        "Please enter a new role (Admin, Teacher, Student, or press Enter to skip)", type=str, default=""
    )
    first_name = click.prompt("Please enter a new first name (or press Enter to skip)", type=str, default="")
    last_name = click.prompt("Please enter a new last name (or press Enter to skip)", type=str, default="")
    email = click.prompt("Please enter a new email (or press Enter to skip)", type=str, default="")

    # Prepare user data for update
    user_data = {
        "user_id": user_id,
        "username": username,
        "role": role,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
    }

    # Remove any fields that were not updated (i.e., left blank)
    user_data = {k: v for k, v in user_data.items() if v}

    # Send PUT request to update the user
    response = requests.put(f"{API_BASE_URL}/users/{user_id}", json=user_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to create a new module
def create_module() -> None:
    """
    Creates a new module in the LMS system.
    Prompts the user to enter module details.
    Sends a POST request to the LMS API to create the module.
    """
    # Get module details
    title = click.prompt("Please enter the module title", type=str)
    description = click.prompt("Please enter the module description", type=str)
    click.echo("")

    # Prepare module data
    module_data = {"title": title, "description": description}

    # Send POST request to create the module
    response = requests.post(f"{API_BASE_URL}/modules/create", json=module_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to create a new assignment
def create_assignment() -> None:
    """
    Creates a new assignment in the LMS system.
    Retrieves the list of modules and prompts the user to select a module to add the assignment to.
    Prompts the user to enter assignment details.
    Sends a POST request to the LMS API to create the assignment.
    """
    # Display list of available modules
    click.echo("List of available modules to add an assignment to")
    response = requests.get(f"{API_BASE_URL}/modules/list")
    data = response.json()

    # Check if the response is an error message
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        # Display the list of modules
        click.echo("")
        click.echo("Current modules in the system:")
        for module in data:
            click.echo(f'- Module ID: {module.get("id")}. Title: {module.get("title")}')
    click.echo("")

    # Get assignment details
    title = click.prompt("Please enter the assignment title", type=str)
    description = click.prompt("Please enter the assignment description", type=str)
    module_id = click.prompt("Please enter the module ID", type=int)
    due_date = click.prompt("Please enter the due date (YYYY-MM-DD)", type=str)
    click.echo("")

    # Prepare assignment data
    assignment_data = {"title": title, "description": description, "module_id": module_id, "due_date": due_date}

    # Send POST request to create the assignment
    response = requests.post(f"{API_BASE_URL}/assignments/create", json=assignment_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to submit a grade
def submit_grade() -> None:
    """
    Submits a grade for a student in a particular assignment.
    Retrieves lists of students and assignments and prompts the user to select a student and an assignment.
    Prompts the user to enter the score.
    Sends a POST request to the LMS API to submit the grade.
    """
    # Display list of available students
    click.echo("List of available students")
    response = requests.get(f"{API_BASE_URL}/users/list_students")
    data = response.json()

    # Check if the response is an error message
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        # Display the list of students
        click.echo("")
        click.echo("Current students in the system:")
        for student in data:
            click.echo(
                f'- Student ID: {student.get("id")}. Name: {student.get("first_name")} - {student.get("last_name")}'
            )

    # Retrieve and display the list of assignments
    response = requests.get(f"{API_BASE_URL}/assignments/list")
    data = response.json()
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        click.echo("")
        click.echo("Current assignments in the system:")
        for assignment in data:
            click.echo(f'- Assignment ID: {assignment.get("id")}. Title: {assignment.get("title")}')

    # Get grade details
    student_id = click.prompt("Please enter the student ID", type=int)
    assignment_id = click.prompt("Please enter the assignment ID", type=int)
    score = click.prompt("Please enter the score", type=float)
    click.echo("")

    # Prepare grade data
    grade_data = {"student_id": student_id, "assignment_id": assignment_id, "score": score}

    # Send POST request to submit the grade
    response = requests.post(f"{API_BASE_URL}/grades/create", json=grade_data)
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to view grades as a student
def view_grades() -> None:
    """
    Retrieves and displays the grades of the currently logged-in student.
    Sends a GET request to the LMS API to retrieve the grades.
    """
    response = requests.get(f"{API_BASE_URL}/grades/view")
    data = response.json()

    # Check if the response is an error message
    if isinstance(data, dict):
        message = data.get("message")
        click.echo(message)
    else:
        # Display the list of grades
        click.echo("")
        click.echo("Your grades:")
        for grade in data:
            click.echo(f'- Assignment ID: {grade.get("assignment_id")}, Score: {int(grade.get("score"))}/100')
    click.echo("")


# Function to toggle the Hacker Mode feature switch
def toggle_hacker_mode() -> None:
    """
    Toggles the Hacker Mode feature switch.
    Prompts the user to turn Hacker Mode on or off.
    Sends a POST request to the LMS API to update the Hacker Mode status.
    """
    click.echo("Toggle Hacker Mode")
    status = click.prompt("Enter 1 to turn ON or 0 to turn OFF", type=int)

    # Validate input
    if status not in {0, 1}:
        click.echo("Invalid input. Please enter 1 or 0.")
        return

    # Send POST request to toggle Hacker Mode
    response = requests.post(f"{API_BASE_URL}/feature_switch/hacker_mode", json={"active": status})
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Function to log out of the LMS system
def logout() -> None:
    """
    Logs out of the LMS system.
    Sends a PUT request to the LMS API to log out.
    """
    click.echo("")
    response = requests.put(f"{API_BASE_URL}/logout")
    data = response.json()
    message = data.get("message")
    click.echo(message)
    click.echo("")


# Main entry point for the script
if __name__ == "__main__":
    cli()

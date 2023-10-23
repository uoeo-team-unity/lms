# Team Unity - LMS application

## Welcome

Welcome to the Team Unity LMS application repository. This project is the repository for the LMS application.

## Running with docker

Make sure you have Docker running locally. If not, you can download the desktop application from the [Docker website](https://www.docker.com/products/docker-desktop/).

Create a configuration file by copying the example file:
```bash
cp .env.example .env
```

Spin up the application using Docker Compose:
```bash
docker compose up
```

If you want to enable hot-reload and debugging, create a launch.json file inside the .vscode folder with the following content:
```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Flask via Docker",
            "type": "python",
            "request": "attach",
            "port": 5678,
            "host": "0.0.0.0",
            "pathMappings": [
                {
                    "localRoot": "${workspaceFolder}",
                    "remoteRoot": "/app"
                }
            ]
        }
    ]
}
```

Run tests with this command:

```bash
docker exec -it lms python3 -m pytest -v
```

To run tests with coverage, use this command:
```bash
docker exec -it lms python3 -m pytest --cov=lms tests/
```

Launch the CLI App. By default, an admin user is created for ease of use (username: admin, password: admin):
```bash
docker exec -it lms python3 cli.py
```

You're good to go 🎉
<br>
You're all set! You can now select "Flask via Docker" in your editor's Run and Debug tab and start debugging. 🤗


To stop Docker Compose, use this command:

```bash
docker-compose down -v --remove-orphans
```

## Running without docker-compose
### Prerequisites

Make sure you have Python 3.11 installed on your computer. You can download the latest version either via [pyenv](https://github.com/pyenv/pyenv) or from the [Python website](https://www.python.org/downloads/).

### Install Python via pyenv
Follow [these instructions](https://github.com/pyenv/pyenv#installation) to install pyenv, and follow steps 2, 3 and 4

Install Python (we currently use version 3.11.6) and make it your default version:

```bash
pyenv install 3.11.6
pyenv global 3.11.6
```

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the Python requirements:

```bash
python3 -m pip install -r requirements.txt -r tests/requirements.txt
```

### Run the Application

You should now be able to run the app locally:

<details>
<summary>Visual Studio Code configuration</summary>

Create a new `launch.json` file inside the `.vscode` folder with the following content:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "lms/app.py",
                "FLASK_ENV": "development",
                "DEBUG": "1"
            },
            "args": [
                "run",
                "--port=5002"
            ],
            "jinja": true
        }
    ]
}
```

You will then be able to start the application via the debugger.

Start the application via the debugger in Visual Studio Code.

The application should be running at [http://127.0.0.1:5002](http://127.0.0.1:5002).

</details>

<details>
<summary>Other editors</summary>

If you are using other code editors, you can run the application using the following command:
```bash
flask --app lms.app run
```

The application should be running at [http://127.0.0.1:5000](http://127.0.0.1:5000).
</details>

<br>

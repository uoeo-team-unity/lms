import json

import pytest

from tests.factories import ModuleFactory


@pytest.mark.usefixtures("wipe_modules_table")
class TestModule:
    def test_create_module(self, client, teacher_user) -> None:
        # Test creating a module by a teacher
        module = ModuleFactory.build()

        params = {"title": module.title, "description": module.description, "teacher_id": module.teacher_id}

        response = client.post("/modules/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data.get("message") == f"Module with title {module.title} successfully created"

    def test_create_module_with_hacker_mode(self, client, teacher_user_without_token, toggle_hacker_mode) -> None:
        # Test creating a module with hacker mode enabled
        module = ModuleFactory.build()

        params = {"title": module.title, "description": module.description, "teacher_id": module.teacher_id}

        response = client.post("/modules/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 201
        assert data.get("message") == f"Module with title {module.title} successfully created"

    def test_create_module_with_missing_argument(self, client, teacher_user) -> None:
        # Test creating a module with missing arguments
        module = ModuleFactory.build()

        params = {"description": module.description, "teacher_id": module.teacher_id}

        response = client.post("/modules/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 422
        assert data.get("message") == "Something doesn't look right, please double-check the parameters and try again"

    def test_create_module_as_a_student(self, client, student_user) -> None:
        # Test creating a module by a student (unauthorized)
        module = ModuleFactory.build()

        params = {"title": module.title, "description": module.description, "teacher_id": module.teacher_id}

        response = client.post("/modules/create", json=params)
        data = json.loads(response.data)

        assert response.status_code == 401
        assert data.get("message") == (
            "It appears you are not authorised to perform this action. "
            "Please double-check your authorisation and try again."
        )

    def test_list_all_modules_as_a_teacher(self, client, teacher_user) -> None:
        # Test listing all modules as a teacher
        ModuleFactory.create()
        ModuleFactory.create()

        response = client.get("/modules/list")
        data = json.loads(response.data)

        assert response.status_code == 200

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "title" in data[0]

    def test_list_all_modules_as_a_student(self, client, student_user) -> None:
        # Test listing all modules as a student (unauthorized)
        ModuleFactory.create()
        ModuleFactory.create()

        response = client.get("/modules/list")
        data = json.loads(response.data)

        assert response.status_code == 401

        assert data == {
            "message": (
                "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            )
        }

    def test_list_all_modules_with_hacker_mode(self, client, teacher_user_without_token, toggle_hacker_mode) -> None:
        # Test listing all modules with hacker mode enabled
        ModuleFactory.create()
        ModuleFactory.create()

        response = client.get("/modules/list")
        data = json.loads(response.data)

        assert response.status_code == 200

        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "title" in data[0]

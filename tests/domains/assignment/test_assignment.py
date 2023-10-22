import json

import pytest

from tests.factories import AssignmentFactory, ModuleFactory


@pytest.mark.usefixtures("wipe_assignments_table")
class TestAssignment:
    def test_create_assignment(self, client, teacher_user) -> None:
        # Test creating an assignment
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()
        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }
        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data.get("message") == f"Assignment with title {assignment.title} successfully created"

    def test_create_assignment_with_hacker_mode(self, client, teacher_user_without_token, toggle_hacker_mode) -> None:
        # Test creating an assignment with hacker mode enabled
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()
        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }
        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)
        assert response.status_code == 201
        assert data.get("message") == f"Assignment with title {assignment.title} successfully created"

    def test_create_assignment_with_missing_argument(self, client, teacher_user) -> None:
        # Test creating an assignment with missing argument
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()
        params = {
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }
        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)
        assert response.status_code == 422
        assert data.get("message") == "Something doesn't look right, please double check the parameters and try again"

    def test_create_assignment_as_a_student(self, client, student_user) -> None:
        # Test creating an assignment as a student
        assignment = AssignmentFactory.build()
        module = ModuleFactory.create()
        params = {
            "title": assignment.title,
            "description": assignment.description,
            "module_id": module.id,
            "due_date": assignment.due_date,
        }
        response = client.post("/assignments/create", json=params)
        data = json.loads(response.data)
        assert response.status_code == 401
        assert data.get("message") == (
            "It appears you are not authorised to perform this action. "
            "Please double-check your authorisation and try again."
        )

    def test_list_all_assignments_as_a_teacher(self, client, teacher_user) -> None:
        # Test listing all assignments as a teacher
        AssignmentFactory.create()
        AssignmentFactory.create()
        response = client.get("/assignments/list")
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "title" in data[0]

    def test_list_all_assignments_with_hacker_mode(
        self, client, teacher_user_without_token, toggle_hacker_mode
    ) -> None:
        # Test listing all assignments with hacker mode enabled
        AssignmentFactory.create()
        AssignmentFactory.create()
        response = client.get("/assignments/list")
        data = json.loads(response.data)
        assert isinstance(data, list)
        assert len(data) >= 1
        assert "id" in data[0]
        assert "title" in data[0]

    def test_list_all_users_as_a_student(self, client, student_user) -> None:
        # Test listing all assignments as a student
        AssignmentFactory.create()
        AssignmentFactory.create()
        response = client.get("/assignments/list")
        data = json.loads(response.data)
        assert response.status_code == 401
        assert data == {
            "message": (
                "It appears you are not authorised to perform this action. "
                "Please double-check your authorisation and try again."
            )
        }

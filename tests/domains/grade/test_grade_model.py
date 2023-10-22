import pytest

from lms.domains import Grade
from tests.factories import AssignmentFactory, GradeFactory, UserFactory


@pytest.mark.usefixtures("wipe_grades_table")
class TestGradeModel:
    def test_grade_init(self) -> None:
        # Test the initialisation of a Grade object
        grade = GradeFactory.build()
        assert isinstance(grade, Grade)
        assert isinstance(grade.score, (int, type(None)))
        assert isinstance(grade.student_id, (int, type(None)))
        assert isinstance(grade.assignment_id, (int, type(None)))

    def test_grade_init_with_missing_value(self) -> None:
        # Test the initialisation of a Grade object with missing values
        with pytest.raises(TypeError) as error:
            Grade()

        assert str(error.value) == (
            "__init__() missing 3 required positional arguments: 'score', 'student_id', and 'assignment_id'"
        )

    def test_grade_create(self) -> None:
        # Test creating a Grade object
        student = UserFactory.create()
        assignment = AssignmentFactory.create()
        grade = GradeFactory.build(student_id=student.id, assignment_id=assignment.id)
        created_grade = Grade.create(score=grade.score, student_id=grade.student_id, assignment_id=grade.assignment_id)

        assert isinstance(created_grade, Grade)
        assert created_grade.score == grade.score

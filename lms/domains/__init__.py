# Importing necessary classes and functions from different modules within the same package

from .assignment import Assignment, AssignmentService, assignment_domain
from .feature_switch import FeatureSwitch, feature_switch_domain
from .grade import Grade, GradeService, grade_domain
from .module import Module, ModuleService, module_domain
from .user import User, UserRole, UserService, user_domain

# Defining a list of public objects that should be accessible when this package is imported

__all__ = [
    "assignment_domain",
    "Assignment",
    "AssignmentService",
    "FeatureSwitch",
    "feature_switch_domain",
    "Grade",
    "GradeService",
    "grade_domain",
    "User",
    "UserRole",
    "user_domain",
    "UserService",
    "Module",
    "ModuleService",
    "module_domain",
]

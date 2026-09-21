from enum import Enum

class ProjectRole(str, Enum):
    ADMIN = "ADMIN"
    QA_ENGINEER = "QA_ENGINEER"
    DEVELOPER = "DEVELOPER"
    VIEWER = "VIEWER"
from enum import Enum

class SystemRole(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"
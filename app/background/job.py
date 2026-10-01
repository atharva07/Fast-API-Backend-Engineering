from dataclasses import dataclass
from enum import Enum

class JobStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"

@dataclass
class TestExecutionJob:
    test_case_id: int
    result_id: int
    attempts: int = 0
    status: JobStatus = JobStatus.PENDING
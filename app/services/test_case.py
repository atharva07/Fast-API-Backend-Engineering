from sqlalchemy.orm import Session
from app.db.models.test_case import TestCase
from app.db.models.test_result import TestResult
from app.repositories.test_case import TestCaseRepository
from app.exceptions.test_case import (
    TestCaseNotExecutableError, TestCaseNotFoundError
)
from app.db.models.audit_log import Auditlog
from app.repositories.audit_log import AuditLogRepository
from app.db.unit_of_work import UnitOfWork

class TestCaseService:
    def __init__(
        self, 
        uow: UnitOfWork
    ):
        self.uow = uow

    def execute_test_case(
        self,
        test_case_id: int,
    ) -> TestResult:
        test_case = self.uow.test_cases.get_by_id(
            test_case_id
        )

        if test_case is None:
            raise TestCaseNotFoundError(
                "Test Case not found"
            )

        if test_case.status != "ACTIVE":
            raise TestCaseNotExecutableError(
                "Only Active Test Cases can be executed"
            )

        result = TestResult(
            test_case_id=test_case.id,
            status="RUNNING"
        )

        self.uow.db.add(result)

        audit_log = Auditlog(
            test_case_id=test_case.id,
            action="TEST_EXECUTION_STARTED"
        )

        self.uow.audit_logs.add(audit_log)

        self.uow.commit()

        self.uow.db.refresh(result)

        return result
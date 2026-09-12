from sqlalchemy.orm import Session
from app.db.models.test_case import TestCase
from app.db.models.test_result import TestResult
from app.repositories.test_case import TestCaseRepository
from app.exceptions.test_case import (
    TestCaseNotExecutableError, TestCaseNotFoundError
)

class TestCaseService:
    def __init__(self, db: Session):
        self.db = db
        self.respository = TestCaseRepository(db)

    def execute_test_case(
        self,
        test_case_id: int,
    ) -> TestResult:
        test_case = self.respository.get_by_id(
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
            status="RUNIING"
        )

        self.db.add(result)
        self.db.commit()
        self.db.refresh(result)

        return result
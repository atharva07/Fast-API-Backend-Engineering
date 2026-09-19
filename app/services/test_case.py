from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.db.models.test_case import TestCase
from app.db.models.test_result import TestResult
from app.models.test_case import Priority
from app.repositories.test_case import TestCaseRepository
from app.exceptions.test_case import (
    TestCaseNotExecutableError, TestCaseNotFoundError, TestCaseAlreadyExistsError
)
from app.exceptions.test_suite import TestSuiteNotFoundError
from app.db.models.audit_log import Auditlog
from app.repositories.audit_log import AuditLogRepository
from app.db.unit_of_work import UnitOfWork

class TestCaseService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    def execute_test_case(self, test_case_id: int) -> TestResult:
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

        result = TestResult(test_case_id=test_case.id, status="RUNNING")

        self.uow.db.add(result)
        audit_log = Auditlog(test_case_id=test_case.id, action="TEST_EXECUTION_STARTED")
        self.uow.audit_logs.add(audit_log)
        self.uow.commit()
        self.uow.db.refresh(result)

        return result

    """
        This is GET Request
    """
    def get_test_cases_by_suite(self, suite_id: int) -> list[TestCase]:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            return self.uow.test_cases.get_by_suite(suite_id)

    """
        This is POST Request
    """
    def create_test_case(self, suite_id: int, name: str, description: str | None, priority: str) -> TestCase:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            test_case = TestCase(
                name=name,
                description=description,
                priority=priority,
                suite_id=suite_id,
            )

            self.uow.test_cases.add(test_case)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise TestCaseAlreadyExistsError("A Test case with this name already Exists")
                raise

            return test_case

    """
        This is GET Request
    """
    def get_test_case(self, test_case_id: int) -> TestCase:
        with self.uow:
            test_case = self.uow.test_cases.get_by_id(test_case_id)

            if test_case is None:
                raise TestCaseNotFoundError("Test Case Not Found")

            return test_case

    """
        This is a PUT Request
    """
    def replace_test_case(self, test_case_id: int, name: str, description: str | None, priority: str) -> TestCase:
        with self.uow:
            test_case = self.uow.test_cases.get_by_id(test_case_id)

            if test_case is None:
                raise TestCaseNotFoundError("Test Case Not Found")

            test_case.name = name
            test_case.description = description
            test_case.priority = priority

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.commit()

                if exc.orig.sqlstate == "23505":
                    raise TestCaseAlreadyExistsError("A Test case with this name already exists")
                raise

            return test_case

    """
        This is a PATCH Request
    """
    def update_test_case(self, test_case_id: int, name: str | None, description: str | None, priority: str) -> TestCase:
        with self.uow:
            test_case = self.uow.test_cases.get_by_id(test_case_id)

            if test_case is None:
                raise TestCaseNotFoundError("Test Case Not Found")

            if name is not None:
                test_case.name = name

            if description is not None:
                test_case.description = description

            if priority is not None:
                test_case.priority = priority

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.commit()

                if exc.orig.sqlstate == "23505":
                    raise TestCaseAlreadyExistsError("A Test case with this name already exists")
                raise

            return test_case

    """
        This is DELETE Request
    """
    def delete_test_case(self, test_case_id: int) -> None:
        with self.uow:
            test_case = self.uow.test_cases.get_by_id(test_case_id)

            if test_case is None:
                raise TestCaseNotFoundError("Test Case Not Found")

            self.uow.test_cases.delete(test_case)

            self.uow.commit()
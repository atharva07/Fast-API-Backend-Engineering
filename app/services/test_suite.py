from app.db.models.test_suite import TestSuite
from app.db.unit_of_work import UnitOfWork
from app.exceptions.project import ProjectNotFoundError
from app.exceptions.test_suite import TestSuiteAlreadyExistsError, TestSuiteNotFoundError
from sqlalchemy.exc import IntegrityError

class TestSuiteService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    """
        This is a POST Request
    """
    def create_suite(self, project_id: int, name: str, description: str | None = None) -> TestSuite:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            suite = TestSuite(name=name, description=description, project_id=project_id)

            self.uow.test_suites.add(suite)

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise TestSuiteAlreadyExistsError("A Test Suite with this name already Exists")
                raise

            return suite

    """
        This is a GET Request
    """
    def get_suites(self, project_id: int) -> list[TestSuite]:
        with self.uow:
            project = self.uow.projects.get_by_id(project_id)

            if project is None:
                raise ProjectNotFoundError("Project Not Found")

            return self.uow.test_suites.get_by_project(project_id)

    """
        This is a GET Request
    """
    def get_suite(self, suite_id: int) -> TestSuite:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            return suite

    """
        This is a PATCH Request
    """
    def update_suite(self, suite_id: int, name: str | None, description: str | None) -> TestSuite:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            if name is not None:
                suite.name = name

            if description is not None:
                suite.description = description

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise TestSuiteAlreadyExistsError("A Test Suite with this name already Exists")
                raise

            return suite

    """
        This is a PATCH Request
    """
    def replace_suite(self, suite_id: int, name: str | None, description: str | None) -> TestSuite:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            suite.name = name
            suite.description = description

            try:
                self.uow.commit()
            except IntegrityError as exc:
                self.uow.rollback()

                if exc.orig.sqlstate == "23505":
                    raise TestSuiteAlreadyExistsError("A Test Suite with this name already Exists")
                raise

            return suite

    """
        This is a DELETE Request
    """
    def delete_suite(self, suite_id: int) -> None:
        with self.uow:
            suite = self.uow.test_suites.get_by_id(suite_id)

            if suite is None:
                raise TestSuiteNotFoundError("Test Suite Not Found")

            self.uow.test_suites.delete(suite)

            self.uow.commit()
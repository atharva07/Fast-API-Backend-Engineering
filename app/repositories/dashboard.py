from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.db.models.project import Project
from app.db.models.test_suite import TestSuite
from app.db.models.test_case import TestCase
from app.db.models.test_result import TestResult
from app.db.models.associations import ProjectUser

class DashboardRepository:
    def __init__(self, db: Session):
        self.db = db

    def count_projects(self, user_id: int, is_admin: bool) -> int:
        query = select(func.count(Project.id))

        if not is_admin:
            query = (
                query
                .join(
                    ProjectUser,
                    ProjectUser.project_id == Project.id,
                )
                .where(ProjectUser.user_id == user_id)
            )

        return self.db.execute(query).scalar_one()

    def count_test_suites(
        self,
        user_id: int,
        is_admin: bool
    ) -> int:
        query = select(func.count(TestSuite.id))

        if not is_admin:
            query = (
                query
                .join(
                    ProjectUser,
                    ProjectUser.project_id == TestSuite.project_id
                )
                .where(ProjectUser.user_id == user_id)
            )

        return self.db.execute(query).scalar_one()

    def count_test_cases(
        self,
        user_id: int,
        is_admin: bool
    ) -> int:
        query = (
            select(func.count(TestCase.id))
            .join(
                TestSuite,
                TestCase.suite_id == TestSuite.id,
            )
        )

        if not is_admin:
            query = (
                query
                .join(
                    ProjectUser,
                    ProjectUser.project_id == TestSuite.project_id
                )
                .where(ProjectUser.user_id == user_id)
            )

        return self.db.execute(query).scalar_one()

    def count_executions(
        self,
        user_id: int,
        is_admin: bool
    ) -> int:
        query = (
            select(func.count(TestResult.id))
            .join(
                TestCase,
                TestResult.test_case_id == TestCase.id,
            )
            .join(
                TestSuite,
                TestCase.suite_id == TestSuite.id
            )
        )

        if not is_admin:
            query = (
                query
                .join(
                    ProjectUser,
                    ProjectUser.project_id == TestSuite.project_id
                )
                .where(ProjectUser.user_id == user_id)
            )

        return self.db.execute(query).scalar_one()
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.test_suite import TestSuite

class TestSuiteRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, suite_id: int) -> TestSuite | None:
        return self.db.execute(select(TestSuite).where(TestSuite.id == suite_id)).scalar_one_or_none()

    def get_by_project(self, project_id: int) -> list[TestSuite]:
        return self.db.execute(select(TestSuite).where(TestSuite.project_id == project_id)).scalars().all()

    def add(self, suite: TestSuite) -> TestSuite:
        self.db.add(suite)

        return suite

    def delete(self, suite: TestSuite) -> None:
        self.db.delete(suite)
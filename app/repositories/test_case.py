from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.test_case import TestCase

class TestCaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(
        self,
        test_case_id: int,
    ) -> TestCase | None:
        return self.db.execute(
            select(TestCase)
            .where(TestCase.id == test_case_id)
        ).scalar_one_or_none()

    def get_all(self) -> list[TestCase]:
        return self.db.execute(
            select(TestCase)
        ).scalars().all()

    def add(
        self,
        test_case: TestCase,
    ) -> TestCase:
        self.db.add(test_case)

        return test_case

    def delete(
        self,
        test_case: TestCase,
    ) -> None:
        self.db.delete(test_case)
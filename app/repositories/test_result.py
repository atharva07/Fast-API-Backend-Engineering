from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models.test_result import TestResult

class TestResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, result_id: int) -> TestResult | None:
        return self.db.execute(
            select(TestResult)
            .where(TestResult.id == result_id)
        ).scalar_one_or_none()

    def get_by_test_case(self, test_case_id: int) -> list[TestResult]:
        return self.db.execute(
            select(TestResult)
            .where(TestResult.test_case_id == test_case_id)
        ).scalars().all()
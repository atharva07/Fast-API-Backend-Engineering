from datetime import datetime, UTC, timedelta
from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.db.models.test_result import TestResult
from app.models.test_result import TestResultStatus

class TestResultRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> list[TestResult]:
        return self.db.execute(
            select(TestResult)
            .order_by(TestResult.id.desc())
        ).scalars().all()

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

    """
        We have applied filtering and pagination on the endpoint. 
        So before pagination comes filtering. Once the filtering is done, pagination is applied on that output
    """
    def get_page(self, offset: int, limit: int, status: TestResultStatus | None = None, test_case_id: int | None = None) -> list[TestResult]:
        query = (
            select(TestResult)
            .order_by(TestResult.id.desc())
        )

        if status is not None:
            query = query.where(
                TestResult.status == status
            )

        if test_case_id is not None:
            query = query.where(
                TestResult.test_case_id == test_case_id
            )

        query = (
            query
            .offset(offset)
            .limit(limit)
        )

        return self.db.execute(query).scalars().all()

    def count_all(self, status: TestResultStatus | None = None, test_case_id: int | None = None) -> int:
        query = select(
            func.count(TestResult.id)
        )

        if status is not None:
            query = query.where(
                TestResult.status == status
            )

        if test_case_id is not None:
            query = query.where(
                TestResult.test_case_id == test_case_id
            )

        return self.db.execute(query).scalar_one()
        
    def claim_execution(self, execution_id: int) -> TestResult | None:
        result = self.db.execute(
            select(TestResult)
            .where(
                TestResult.id == execution_id
            )
            .with_for_update()
        ).scalar_one_or_none()

        if result is None:
            return None

        if result.status != "RUNNING":
            return None

        result.status = "PROCESSING"
        result.processing_started_at = datetime.now(UTC)

        self.db.commit()

        return result

    def reset_stuck_execution(self, timeout_minutes: int = 10) -> list[TestResult]:
        cutoff = datetime.now(UTC) - timedelta(minutes=timeout_minutes)

        results = self.db.execute(
            select(TestResult)
            .where(
                TestResult.status == "PROCESSING",
                TestResult.processing_started_at < cutoff
            )
            .with_for_update(
                skip_locked=True
            )
        ).scalars().all()

        for result in results:
            result.status = "RUNNING"
            result.processing_started_at = None

        self.db.commit()

        return results
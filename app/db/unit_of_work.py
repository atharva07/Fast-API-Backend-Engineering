from sqlalchemy.orm import Session
from app.repositories.audit_log import AuditLogRepository
from app.repositories.test_case import TestCaseRepository

class UnitOfWork:
    def __init__(self, db: Session):
        self.db = db
        self.test_cases = TestCaseRepository(db)
        self.audit_logs = AuditLogRepository(db)

    def __enter__(self):
        return self

    # Three arguments used in below method
    # 1. exc_type: This tells what type of exception occured
    # 2. exc_value: Actual exc object,
    # 3. traceback: This contains information about where the exception happened
    def __exit__(
        self, 
        exc_type, 
        exc_value, 
        traceback
    ):
        if exc_type is not None:
            self.rollback()

    def commit(self) -> None:
        self.db.commit()

    def rollback(self) -> None:
        self.db.rollback()
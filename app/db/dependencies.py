from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.test_case import TestCaseRepository
from app.services.test_case import TestCaseService
from app.repositories.audit_log import AuditLogRepository

def get_db() -> Generator:
    db = SessionLocal()

    print("DATABASE SESSION CREATED")

    try:
        yield db
    finally:
        print("DATABASE SESSION CLOSING")
        db.close()

DBSession = Annotated[Session, Depends(get_db)]

def get_test_case_repository(
    db: DBSession
) -> TestCaseRepository:
    return TestCaseRepository(db)

def get_audit_log_repository(
    db: DBSession
) -> AuditLogRepository:
    return AuditLogRepository(db)

def get_test_case_service(
    db: DBSession,
    repository: TestCaseRepository = Depends(get_test_case_repository),
    audit_repository: AuditLogRepository = Depends(get_audit_log_repository),
) -> TestCaseService:
    return TestCaseService(
        db=db,
        repository=repository,
        audit_repository=audit_repository
    )
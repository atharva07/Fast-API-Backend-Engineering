from collections.abc import Generator
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from app.repositories.test_case import TestCaseRepository
from app.services.test_case import TestCaseService
from app.repositories.audit_log import AuditLogRepository
from app.db.unit_of_work import UnitOfWork

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

def get_unit_of_work(
    db: DBSession,
) -> UnitOfWork:
    return UnitOfWork(db)

def get_test_case_service(
    uow: UnitOfWork = Depends(get_unit_of_work),
) -> TestCaseService:
    return TestCaseService (
        uow = uow
    )
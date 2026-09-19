from sqlalchemy.orm import Session
from app.db.models.audit_log import Auditlog

class AuditLogRepository:
    def __init__(self, db: Session):
        self.db = db

    def add(self, audit_log: Auditlog) -> Auditlog:
        self.db.add(audit_log)

        return audit_log
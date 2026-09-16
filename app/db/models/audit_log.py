from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.database import Base

class Auditlog(Base):
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(
        primary_key=True
    )

    test_case_id: Mapped[int] = mapped_column(
        ForeignKey(
            "test_case.id",
            ondelete="CASCADE",
        ),
        nullable=False
    )

    action: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )
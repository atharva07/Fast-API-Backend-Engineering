from typing import TYPE_CHECKING
from sqlalchemy import Integer, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base

if TYPE_CHECKING:
    from app.db.models.project import Project

class TestSuite(Base):
    __tablename__ = "test_suites"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        unique=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    """
    This means that that, if we delete the project then it will also the test suites associated with the proiect. This is because test suites are child and cannot be 
    exist without parent, which is project
    """
    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    project: Mapped["Project"] = relationship(
        back_populates="test_suites"
    )
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.project import Project
    from app.db.models.user import User

class ProjectUser(Base):
    __tablename__ = "project_users"

    project_id: Mapped[int] = mapped_column(
        ForeignKey(
            "projects.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey(
            "users.id",
            ondelete="CASCADE"
        ),
        primary_key=True
    )

    role: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    # These are ORM relationships

    # A project_user can have one project
    project: Mapped["Project"] = relationship(
        back_populates="project_users"
    )

    user: Mapped["User"] = relationship(
        back_populates="project_users"
    )

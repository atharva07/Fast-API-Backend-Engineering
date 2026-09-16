from sqlalchemy import Column, ForeignKey, Table
from app.db.database import Base

project_users = Table(
    "project_users",
    Base.metadata,
    Column(
        "project_id",
        ForeignKey("projects.id", ondelete="CASCADE"),
        primary_key=True
    ),
    Column(
        "user_id",
        ForeignKey("users.id"),
        primary_key=True
    )
)
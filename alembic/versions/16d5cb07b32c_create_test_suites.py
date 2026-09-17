"""create test suites

Revision ID: 16d5cb07b32c
Revises: f9c6509299b3
Create Date: 2026-09-18 00:07:59.933059

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16d5cb07b32c'
down_revision: Union[str, Sequence[str], None] = 'f9c6509299b3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "test_suites",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("project_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"], ondelete="CASCADE"),
        sa.UniqueConstraint("project_id", "name", name="uq_test_suites_project_name"),
    )

def downgrade() -> None:
    """Downgrade schema."""
    sa.UniqueConstraint(
            "project_id",
            "name",
            name="uq_test_suites_project_name",
        ),

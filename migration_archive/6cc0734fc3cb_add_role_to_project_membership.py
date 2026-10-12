"""add role to project membership

Revision ID: 6cc0734fc3cb
Revises: 39302df35b07
Create Date: 2026-09-21 23:02:47.410235

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6cc0734fc3cb'
down_revision: Union[str, Sequence[str], None] = '39302df35b07'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("project_users", sa.Column("role", sa.String(length=30), nullable=False, server_default="VIEWER"),)
    op.alter_column("project_users", "role", server_default=None)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("project_users", "role")

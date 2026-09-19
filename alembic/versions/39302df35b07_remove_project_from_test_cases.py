"""remove project from test cases

Revision ID: 39302df35b07
Revises: bd4ccb620759
Create Date: 2026-09-19 17:10:58.138391

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '39302df35b07'
down_revision: Union[str, Sequence[str], None] = 'bd4ccb620759'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint("test_case_project_id_fkey", "test_case", type_="foreignkey")
    op.drop_column("test_case", "project_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column("test_case", sa.Column("project_id", sa.Integer(), nullable=True))
    op.create_foreign_key("test_case_project_id_fkey", "test_case", "projects", ["project_id"], ["id"], ondelete="CASCADE")

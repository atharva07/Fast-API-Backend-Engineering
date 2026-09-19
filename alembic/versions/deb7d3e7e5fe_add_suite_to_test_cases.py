"""add suite to test cases

Revision ID: deb7d3e7e5fe
Revises: 16d5cb07b32c
Create Date: 2026-09-19 03:04:39.974788

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'deb7d3e7e5fe'
down_revision: Union[str, Sequence[str], None] = '16d5cb07b32c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column("test_case", sa.Column("suite_id", sa.Integer(), nullable=True))
    op.create_foreign_key("test_case_suite_id_fkey", "test_case", "test_suites", ["suite_id"], ["id"], ondelete="CASCADE")
            

def downgrade() -> None:
    """Downgrade schema."""
    pass

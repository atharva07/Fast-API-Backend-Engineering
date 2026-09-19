"""make test case suite required

Revision ID: bd4ccb620759
Revises: deb7d3e7e5fe
Create Date: 2026-09-19 16:26:23.581438

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd4ccb620759'
down_revision: Union[str, Sequence[str], None] = 'deb7d3e7e5fe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column("test_case", "suite_id", existing_type=sa.Integer(), nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column("test_case", "suite_id", existing_type=sa.Integer(), nullable=True)

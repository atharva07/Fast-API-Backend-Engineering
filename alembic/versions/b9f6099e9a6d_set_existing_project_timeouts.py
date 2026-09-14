"""set existing project timeouts

Revision ID: b9f6099e9a6d
Revises: 88152b566b2d
Create Date: 2026-09-15 02:07:11.064169

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9f6099e9a6d'
down_revision: Union[str, Sequence[str], None] = '88152b566b2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute(
        """
        UPDATE projects
        SET execution_timeout = 600
        """
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(
        """
        UPDATE projects
        SET execution_timeout = 3000
        """
    )

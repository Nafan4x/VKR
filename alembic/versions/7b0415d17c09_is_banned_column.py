"""is_banned_column

Revision ID: 7b0415d17c09
Revises: 00b6a60e7de6
Create Date: 2026-02-25 15:38:32.608362

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7b0415d17c09'
down_revision: Union[str, Sequence[str], None] = '00b6a60e7de6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass

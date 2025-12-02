"""file_date

Revision ID: b8b87e8db40b
Revises: ccdf835ab1a8
Create Date: 2025-12-02 13:12:36.669289

"""
from typing import Sequence, Union


from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision: str = 'b8b87e8db40b'
down_revision: Union[str, Sequence[str], None] = 'ccdf835ab1a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # 1. Добавляем колонку без server_default
    op.add_column(
        'resources',
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )

    # 2. Заполняем created_at для существующих записей (опционально)
    now = datetime.utcnow()
    op.execute(f"UPDATE resources SET created_at = '{now.isoformat()}' WHERE created_at IS NULL")

    # 3. Делаем колонку NOT NULL
    op.alter_column('resources', 'created_at', nullable=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('resources', 'created_at')

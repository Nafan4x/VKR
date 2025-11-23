"""feedback_model_unique_fix

Revision ID: 23fd9e81c73b
Revises: 2fc921b041bd
Create Date: 2025-11-22 16:26:04.029288
"""

from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '23fd9e81c73b'
down_revision: Union[str, Sequence[str], None] = '2fc921b041bd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # 🔥 Полная реконструкция таблицы для SQLite batch mode
    with op.batch_alter_table('feedback', recreate='always') as batch_op:
        batch_op.alter_column(
            'from_user_id',
            existing_type=sa.BigInteger(),
            nullable=False,
            unique=False  # 👈 убираем уникальность
        )


def downgrade():
    # Если откатываем – возвращаем unique=True
    with op.batch_alter_table('feedback', recreate='always') as batch_op:
        batch_op.alter_column(
            'from_user_id',
            existing_type=sa.BigInteger(),
            nullable=False,
            unique=True
        )

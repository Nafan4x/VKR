"""seed users table

Revision ID: c497c01c3b05
Revises: 10d07db05f77
Create Date: 2025-11-18 20:27:09.820040

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c497c01c3b05'
down_revision: Union[str, Sequence[str], None] = '10d07db05f77'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # список данных
    data = [
        (1, 'Главная', 'main_page'),
        (2, 'Как вступить?', 'join_page'),
        (3, 'Социальные программы', 'social_page'),
        (4, 'Мероприятия', 'event_page'),
        (5, 'Как связаться?', 'contact_page'),
        (6, 'Обратная связь', 'feedback_page'),
        (6, 'Номер билета', 'member_card_page'),
    ]

    # вставка с проверкой на существование
    for id_, page_name, callback_text in data:
        op.execute(
            sa.text(
                """
                INSERT INTO message (id, page_name, callback_text, text)
                SELECT :id, :page_name, :callback_text, 'В разработке'
                WHERE NOT EXISTS (
                    SELECT 1 FROM message WHERE id = :id
                );
                """
            ).bindparams(
                id=id_,
                page_name=page_name,
                callback_text=callback_text
            )
        )


def downgrade():
    # удаляем только те строки, которые мы создавали
    op.execute(
        """
        DELETE FROM message WHERE id IN (1, 2, 3, 4, 5, 6);
        """
    )
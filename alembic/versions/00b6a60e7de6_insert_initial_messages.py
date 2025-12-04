"""Insert initial messages

Revision ID: 00b6a60e7de6
Revises: ca2db034fb51
Create Date: 2025-12-02 13:52:03.295241

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '00b6a60e7de6'
down_revision: Union[str, Sequence[str], None] = 'ca2db034fb51'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   # список данных
    data = [
        (1, 'Главная', 'main_page'),
        (2, 'Как вступить?', 'join_page'),
        (3, 'Социальные программы', 'social_page'),
        (4, 'Мероприятия', 'event_page'),
        (5, 'Как связаться?', 'contact_page'),
        (6, 'Обратная связь', 'feedback_page'),
        (7, 'Номер билета', 'member_card_page'),
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
    pass


def downgrade() -> None:
    op.execute(
        """
        DELETE FROM message WHERE id IN (1, 2, 3, 4, 5, 6, 7);
        """
    )

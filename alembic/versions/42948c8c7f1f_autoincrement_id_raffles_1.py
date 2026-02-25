"""autoincrement id raffles 1

Revision ID: 42948c8c7f1f
Revises: 5f8b4eca45c2
Create Date: 2026-02-25 16:51:25.899223

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42948c8c7f1f'
down_revision: Union[str, Sequence[str], None] = '5f8b4eca45c2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # SQLite не поддерживает прямое изменение колонки на AUTOINCREMENT
    # Нужно создать новую таблицу, скопировать данные и удалить старую
    
    op.execute('''
        CREATE TABLE raffle_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR NOT NULL,
            description VARCHAR,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL
        )
    ''')
    
    # Копируем данные
    op.execute('''
        INSERT INTO raffle_new (id, title, description, start_time, end_time)
        SELECT id, title, description, start_time, end_time FROM raffle
    ''')
    
    # Удаляем старую таблицу и переименовываем новую
    op.execute('DROP TABLE raffle')
    op.execute('ALTER TABLE raffle_new RENAME TO raffle')


def downgrade() -> None:
    # Откат - возвращаем обычный INTEGER PRIMARY KEY
    op.execute('''
        CREATE TABLE raffle_old (
            id INTEGER PRIMARY KEY,
            title VARCHAR NOT NULL,
            description VARCHAR,
            start_time DATETIME NOT NULL,
            end_time DATETIME NOT NULL
        )
    ''')
    
    op.execute('''
        INSERT INTO raffle_old (id, title, description, start_time, end_time)
        SELECT id, title, description, start_time, end_time FROM raffle
    ''')
    
    op.execute('DROP TABLE raffle')
    op.execute('ALTER TABLE raffle_old RENAME TO raffle')
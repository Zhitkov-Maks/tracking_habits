"""Add field user_chat_id by model  Remind

Revision ID: 5da6d7258381
Revises: 228bf4588c96
Create Date: 2024-12-11 19:43:20.943334

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = '5da6d7258381'
down_revision: Union[str, None] = '228bf4588c96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminds', sa.Column('user_chat_id', mysql.BIGINT(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reminds', 'user_chat_id')
    # ### end Alembic commands ###

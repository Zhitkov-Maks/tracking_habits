"""add field end_date

Revision ID: 3fc693503021
Revises: ba785a97f16c
Create Date: 2024-09-03 21:26:15.173511

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3fc693503021'
down_revision: Union[str, None] = 'ba785a97f16c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('habits', sa.Column('end_date', sa.Date(), server_default='2024-09-24', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('habits', 'end_date')
    # ### end Alembic commands ###
"""change field datetime on date

Revision ID: 014097625a54
Revises: 7a458cbab56f
Create Date: 2024-08-31 00:14:02.289156

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '014097625a54'
down_revision: Union[str, None] = '7a458cbab56f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint(None, 'trackings', ['date'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'trackings', type_='unique')
    # ### end Alembic commands ###
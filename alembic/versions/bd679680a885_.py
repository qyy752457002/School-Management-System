"""

Revision ID: bd679680a885
Revises: dfda86235813
Create Date: 2024-06-14 10:48:23.064328

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bd679680a885'
down_revision: Union[str, None] = 'dfda86235813'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_course', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment='',
               existing_nullable=True)
    op.alter_column('lfun_education_year', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment='',
               existing_nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_education_year', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    op.alter_column('lfun_course', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment=None,
               existing_comment='',
               existing_nullable=True)
    # ### end Alembic commands ###

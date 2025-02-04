"""

Revision ID: 103eb8c09c43
Revises: 318c0bc979c7
Create Date: 2024-06-04 15:10:55.352756

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '103eb8c09c43'
down_revision: Union[str, None] = '318c0bc979c7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('lfun_course', sa.Column('city', sa.String(length=64), nullable=True, comment='城市'))
    op.add_column('lfun_course', sa.Column('district', sa.String(length=64), nullable=True))
    op.alter_column('lfun_education_year', 'city',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               comment='城市')
    op.alter_column('lfun_education_year', 'district',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               comment='')
    op.add_column('lfun_grade', sa.Column('city', sa.String(length=64), nullable=True, comment='城市'))
    op.add_column('lfun_grade', sa.Column('district', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lfun_grade', 'district')
    op.drop_column('lfun_grade', 'city')
    op.alter_column('lfun_education_year', 'district',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               comment=None,
               existing_comment='')
    op.alter_column('lfun_education_year', 'city',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               comment=None,
               existing_comment='城市')
    op.drop_column('lfun_course', 'district')
    op.drop_column('lfun_course', 'city')
    # ### end Alembic commands ###

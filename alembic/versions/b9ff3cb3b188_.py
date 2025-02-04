"""

Revision ID: b9ff3cb3b188
Revises: c4418916f6e7
Create Date: 2024-06-12 16:46:36.159790

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9ff3cb3b188'
down_revision: Union[str, None] = 'c4418916f6e7'
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
    op.alter_column('lfun_grade', 'sort_number',
               existing_type=sa.INTEGER(),
               comment='排序序号',
               existing_comment='排序',
               existing_nullable=True)
    op.alter_column('lfun_organization', 'org_type',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment='组织分类 行政类等')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_organization', 'org_type',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment='组织分类 行政类等')
    op.alter_column('lfun_grade', 'sort_number',
               existing_type=sa.INTEGER(),
               comment='排序',
               existing_comment='排序序号',
               existing_nullable=True)
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

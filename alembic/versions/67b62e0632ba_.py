"""

Revision ID: 67b62e0632ba
Revises: f06fc6e22ef4
Create Date: 2024-06-14 13:55:46.182821

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '67b62e0632ba'
down_revision: Union[str, None] = 'f06fc6e22ef4'
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
    op.alter_column('lfun_major', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment='',
               existing_nullable=True)
    op.alter_column('lfun_task_progress', 'progress_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_comment='进度ID',
               existing_nullable=False)
    op.alter_column('lfun_task_results', 'result_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(),
               existing_comment='结果ID',
               existing_nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_task_results', 'result_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_comment='结果ID',
               existing_nullable=False)
    op.alter_column('lfun_task_progress', 'progress_id',
               existing_type=sa.String(),
               type_=sa.INTEGER(),
               existing_comment='进度ID',
               existing_nullable=False)
    op.alter_column('lfun_major', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment=None,
               existing_comment='',
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

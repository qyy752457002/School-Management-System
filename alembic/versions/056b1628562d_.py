"""

Revision ID: 056b1628562d
Revises: 22358a37d298
Create Date: 2024-06-07 15:14:21.250175

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '056b1628562d'
down_revision: Union[str, None] = '22358a37d298'
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
    op.add_column('lfun_organization', sa.Column('member_cnt', sa.Integer(), nullable=True, comment='人数'))
    op.add_column('lfun_organization_members', sa.Column('teacher_id', sa.Integer(), nullable=True, comment='教师ID'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('lfun_organization_members', 'teacher_id')
    op.drop_column('lfun_organization', 'member_cnt')
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

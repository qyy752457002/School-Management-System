"""

Revision ID: d586112bc211
Revises: 903673e4c3df
Create Date: 2024-06-05 10:29:06.475640

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd586112bc211'
down_revision: Union[str, None] = '903673e4c3df'
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
    op.alter_column('lfun_grade', 'district',
               existing_type=sa.VARCHAR(length=64),
               comment='',
               existing_nullable=True)
    op.alter_column('lfun_work_flow_define', 'process_description',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment='流程描述')
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 153")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 2")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 150")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 156")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 5")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 149")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 152")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.367384', updated_at='2024-06-05 10:29:06.367384' WHERE lfun_course.id = 1")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 158")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 155")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 151")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 154")
    op.execute("UPDATE lfun_course SET created_at='2024-06-05 10:29:06.417996', updated_at='2024-06-05 10:29:06.417996' WHERE lfun_course.id = 157")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_work_flow_define', 'process_description',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment='流程描述')
    op.alter_column('lfun_grade', 'district',
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
    op.execute('DELETE FROM lfun_course WHERE lfun_course.id = 159')
    op.execute('DELETE FROM lfun_course WHERE lfun_course.id = 160')
    op.execute('DELETE FROM lfun_course WHERE lfun_course.id = 161')
    # ### end Alembic commands ###

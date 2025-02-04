"""

Revision ID: 22358a37d298
Revises: 5c0b4c59bd9c
Create Date: 2024-06-07 14:00:04.824654

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '22358a37d298'
down_revision: Union[str, None] = '5c0b4c59bd9c'
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
    op.alter_column('lfun_institutions', 'create_institution_date',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment='成立年月')
    op.alter_column('lfun_institutions', 'web_url',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment='网址')
    op.alter_column('lfun_institutions', 'institution_category',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 单位分类')
    op.alter_column('lfun_institutions', 'institution_type',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment='单位类型 ')
    op.alter_column('lfun_institutions', 'location_economic_attribute',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 所在地经济属性')
    op.alter_column('lfun_institutions', 'leg_repr_certificatenumber',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 法人证书号')
    op.alter_column('lfun_institutions', 'is_entity',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 是否实体')
    op.alter_column('lfun_institutions', 'membership_no',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 隶属单位号')
    op.alter_column('lfun_institutions', 'membership_category',
               existing_type=sa.VARCHAR(length=64),
               nullable=True,
               existing_comment=' 隶属单位类型')
    op.add_column('lfun_organization', sa.Column('school_id', sa.Integer(), nullable=True, comment='学校ID'))
    op.alter_column('lfun_task_progress', 'last_updated',
               existing_type=sqlalchemy_kingbase.types.TIMESTAMP(),
               nullable=False,
               existing_comment='最后更新时间',
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('lfun_task_progress', 'last_updated',
               existing_type=sqlalchemy_kingbase.types.TIMESTAMP(),
               nullable=True,
               existing_comment='最后更新时间',
               existing_server_default=sa.text('CURRENT_TIMESTAMP'))
    op.drop_column('lfun_organization', 'school_id')
    op.alter_column('lfun_institutions', 'membership_category',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 隶属单位类型')
    op.alter_column('lfun_institutions', 'membership_no',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 隶属单位号')
    op.alter_column('lfun_institutions', 'is_entity',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 是否实体')
    op.alter_column('lfun_institutions', 'leg_repr_certificatenumber',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 法人证书号')
    op.alter_column('lfun_institutions', 'location_economic_attribute',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 所在地经济属性')
    op.alter_column('lfun_institutions', 'institution_type',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment='单位类型 ')
    op.alter_column('lfun_institutions', 'institution_category',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment=' 单位分类')
    op.alter_column('lfun_institutions', 'web_url',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment='网址')
    op.alter_column('lfun_institutions', 'create_institution_date',
               existing_type=sa.VARCHAR(length=64),
               nullable=False,
               existing_comment='成立年月')
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

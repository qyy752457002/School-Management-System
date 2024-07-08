"""Merge heads

Revision ID: d90a835aeed7
Revises: b16e943b436d, f93abb78988a
Create Date: 2024-07-08 12:03:39.574485

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd90a835aeed7'
down_revision: Union[str, None] = ('b16e943b436d', 'f93abb78988a')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

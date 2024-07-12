"""Merge heads

Revision ID: 49a9195fe1bb
Revises: 22d76368adac, d1948ec9a2ef
Create Date: 2024-07-11 16:51:52.054699

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '49a9195fe1bb'
down_revision: Union[str, None] = ('22d76368adac', 'd1948ec9a2ef')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

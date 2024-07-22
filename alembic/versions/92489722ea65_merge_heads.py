"""Merge heads

Revision ID: 92489722ea65
Revises: cfe1085d4785, ee0318e103ba
Create Date: 2024-07-10 13:59:00.063688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '92489722ea65'
down_revision: Union[str, None] = ('cfe1085d4785', 'ee0318e103ba')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

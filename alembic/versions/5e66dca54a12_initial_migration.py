"""Initial migration

Revision ID: 5e66dca54a12
Revises: 52a5c1cb0b53
Create Date: 2024-11-22 21:57:02.223379

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5e66dca54a12'
down_revision: Union[str, None] = '52a5c1cb0b53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

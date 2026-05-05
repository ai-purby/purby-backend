"""rename users.address to users.location

Revision ID: 4386e81f9892
Revises: 04e80cd32e86
Create Date: 2026-05-05 22:20:16.658342

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4386e81f9892'
down_revision: Union[str, Sequence[str], None] = '04e80cd32e86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.alter_column(
        "users",
        "address",
        new_column_name="location",
        existing_type=sa.String(length=30),
        existing_nullable=False,
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.alter_column(
        "users",
        "location",
        new_column_name="address",
        existing_type=sa.String(length=30),
        existing_nullable=False,
    )
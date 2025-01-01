"""Create notes table

Revision ID: 6e60c0f0a29d
Revises: fcaebe8c74fc
Create Date: 2025-01-01 10:48:14.430036

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e60c0f0a29d'
down_revision: Union[str, None] = 'fcaebe8c74fc'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'notes',
        sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
        sa.Column('note', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('temporary_key', sa.String(), unique=True, nullable=False),
    )


def downgrade() -> None:
    op.drop_table('notes')

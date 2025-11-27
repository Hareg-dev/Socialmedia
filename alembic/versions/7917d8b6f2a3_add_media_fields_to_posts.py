"""add_media_fields_to_posts

Revision ID: 7917d8b6f2a3
Revises: f62b50222c30
Create Date: 2025-11-27 09:44:16.909129

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7917d8b6f2a3'
down_revision: Union[str, Sequence[str], None] = 'f62b50222c30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('media_url', sa.String(), nullable=True))
    op.add_column('posts', sa.Column('media_type', sa.String(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'media_type')
    op.drop_column('posts', 'media_url')

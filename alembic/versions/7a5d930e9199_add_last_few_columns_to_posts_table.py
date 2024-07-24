"""add last few columns to posts table

Revision ID: 7a5d930e9199
Revises: ee7544dedbde
Create Date: 2024-07-23 21:16:39.609637

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a5d930e9199'
down_revision: Union[str, None] = 'ee7544dedbde'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable= False, server_default= 'TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone= True),
                                     nullable= False, server_default= sa.text(
                                         'NOW()')))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass

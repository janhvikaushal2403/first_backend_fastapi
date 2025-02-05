"""create content cloumn to posts table

Revision ID: 2534a5336dea
Revises: 08fd2505e141
Create Date: 2024-07-23 20:35:39.277147

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2534a5336dea'
down_revision: Union[str, None] = '08fd2505e141'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content',sa.String(), nullable = False))
     
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass

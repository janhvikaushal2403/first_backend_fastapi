"""create posts table

Revision ID: 08fd2505e141
Revises: 
Create Date: 2024-07-23 16:32:18.023959

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '08fd2505e141'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None :
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key= True ),
                    sa.Column('title', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    pass
   
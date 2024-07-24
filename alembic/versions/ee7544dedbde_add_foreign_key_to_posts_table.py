"""add foreign key to posts table

Revision ID: ee7544dedbde
Revises: 300276758367
Create Date: 2024-07-23 21:02:52.946441

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee7544dedbde'
down_revision: Union[str, None] = '300276758367'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key('post_users_fk', source_table= "posts", referent_table="users",
                          local_cols= ["owner_id"], remote_cols= ['id'], ondelete= "CASCADE")        
    pass
# remote col is id field of user table

def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name= "posts")
    op.drop_column('posts', 'owner_id')
    pass

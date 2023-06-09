"""empty message

Revision ID: a2bd28fd0246
Revises: b1e4d0ae5b45
Create Date: 2023-04-14 16:42:26.067087

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a2bd28fd0246'
down_revision = 'b1e4d0ae5b45'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('name', table_name='user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index('name', 'user', ['name'], unique=False)
    # ### end Alembic commands ###

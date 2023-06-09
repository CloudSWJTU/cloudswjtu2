"""empty message

Revision ID: 9e3a0ae94538
Revises: 7ee37154c2ce
Create Date: 2023-05-24 16:08:06.594029

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e3a0ae94538'
down_revision = '7ee37154c2ce'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('video',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('title', sa.String(length=2048), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.Column('url', sa.String(length=4096), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('video')
    # ### end Alembic commands ###

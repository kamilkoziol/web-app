"""empty message

Revision ID: 74573fe21239
Revises: c6e09adcc161
Create Date: 2021-01-30 00:35:13.995376

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '74573fe21239'
down_revision = 'c6e09adcc161'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('about_me', sa.String(length=140), nullable=True))
    op.add_column('user', sa.Column('last_seen', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'last_seen')
    op.drop_column('user', 'about_me')
    # ### end Alembic commands ###

"""empty message

Revision ID: d2aa5aaa6da7
Revises: 
Create Date: 2023-09-26 11:35:08.406152

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2aa5aaa6da7'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('nickname', sa.String(length=120), nullable=True))
    op.add_column('Users', sa.Column('points', sa.Integer(), nullable=True))
    op.create_unique_constraint(None, 'Users', ['nickname'])
    op.drop_column('Users', 'email')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Users', sa.Column('email', sa.VARCHAR(length=120), nullable=True))
    op.drop_constraint(None, 'Users', type_='unique')
    op.drop_column('Users', 'points')
    op.drop_column('Users', 'nickname')
    # ### end Alembic commands ###
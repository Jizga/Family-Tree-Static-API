"""empty message

Revision ID: 9d1061d8e1d5
Revises: 6b8c175d97c4
Create Date: 2021-07-19 18:23:30.936604

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9d1061d8e1d5'
down_revision = '6b8c175d97c4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('person',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('last_name', sa.String(length=100), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('parent_one_id', sa.Integer(), nullable=True),
    sa.Column('parent_two_id', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('person')
    # ### end Alembic commands ###

"""empty message

Revision ID: 77a3b5305eb4
Revises: 03ee21c7d022
Create Date: 2021-07-24 19:10:20.563405

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '77a3b5305eb4'
down_revision = '03ee21c7d022'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('relations', sa.Column('family_member_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'relations', 'person', ['family_member_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'relations', type_='foreignkey')
    op.drop_column('relations', 'family_member_id')
    # ### end Alembic commands ###

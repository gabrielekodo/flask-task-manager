"""empty message

Revision ID: 53f12ff55522
Revises: 8e291c608016
Create Date: 2022-08-05 15:32:37.637681

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '53f12ff55522'
down_revision = '8e291c608016'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('todos', sa.Column('dueDate', sa.Date(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('todos', 'dueDate')
    # ### end Alembic commands ###

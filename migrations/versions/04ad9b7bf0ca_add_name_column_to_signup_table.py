"""add name column to Signup table

Revision ID: 04ad9b7bf0ca
Revises: 7f6289435046
Create Date: 2024-07-11 12:32:32.393079

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '04ad9b7bf0ca'
down_revision = '7f6289435046'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('signups', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###

"""empty message

Revision ID: dfcccf45c6cf
Revises: 7d513ee54b48
Create Date: 2018-12-26 23:18:31.920499

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfcccf45c6cf'
down_revision = '7d513ee54b48'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('user_id', sa.INTEGER(), nullable=False),
    sa.Column('auth0_id', sa.VARCHAR(length=60), nullable=True),
    sa.Column('name', sa.VARCHAR(), nullable=True),
    sa.Column('created', sa.DATETIME(), nullable=True),
    sa.PrimaryKeyConstraint('user_id')
    )
    # ### end Alembic commands ###
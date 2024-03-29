"""empty message

Revision ID: 56ff76a52924
Revises: b290b132f205
Create Date: 2019-05-14 11:52:23.100347

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '56ff76a52924'
down_revision = 'b290b132f205'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('produtos',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('preco', sa.Integer(), nullable=True),
    sa.Column('peso', sa.Integer(), nullable=True),
    sa.Column('estoque', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('produtos')
    # ### end Alembic commands ###

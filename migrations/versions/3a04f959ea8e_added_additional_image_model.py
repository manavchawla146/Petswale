"""added additional image model

Revision ID: 3a04f959ea8e
Revises: fb80e4a4a79a
Create Date: 2025-04-29 22:54:03.443447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3a04f959ea8e'
down_revision = 'fb80e4a4a79a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('product_images',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('image_url', sa.String(length=200), nullable=False),
    sa.Column('is_primary', sa.Boolean(), nullable=True),
    sa.Column('display_order', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_images')
    # ### end Alembic commands ###

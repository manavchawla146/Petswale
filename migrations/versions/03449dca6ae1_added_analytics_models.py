"""added analytics models

Revision ID: 03449dca6ae1
Revises: a24c10bedce3
Create Date: 2025-04-24 00:29:09.244257

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '03449dca6ae1'
down_revision = 'a24c10bedce3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('sales_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('total_sales', sa.Float(), nullable=True),
    sa.Column('order_count', sa.Integer(), nullable=True),
    sa.Column('avg_order_value', sa.Float(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('page_views',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('page', sa.String(length=128), nullable=False),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('user_agent', sa.String(length=256), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_analytics',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('view_count', sa.Integer(), nullable=True),
    sa.Column('cart_add_count', sa.Integer(), nullable=True),
    sa.Column('purchase_count', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product_views',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('ip_address', sa.String(length=45), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['products.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('product_views')
    op.drop_table('product_analytics')
    op.drop_table('page_views')
    op.drop_table('sales_analytics')
    # ### end Alembic commands ###

"""empty message

Revision ID: cefaee503837
Revises: 71f54e500b9d
Create Date: 2023-04-16 15:21:23.033957

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'cefaee503837'
down_revision = '71f54e500b9d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('author_id', sa.Integer(), nullable=True))
        # batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key(batch_op.f('fk_comment_blog_id_blogs'), 'blogs', ['blog_id'], ['id'])
        batch_op.drop_column('code_id')

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(sa.Column('model', sa.String(length=64), nullable=True))
        batch_op.alter_column('cover_img',
               existing_type=sa.NUMERIC(precision=64),
               type_=sa.String(length=64),
               existing_nullable=True)
        batch_op.alter_column('product_route',
               existing_type=sa.NUMERIC(precision=64),
               type_=sa.String(length=64),
               existing_nullable=True)

    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('product_id',
               existing_type=sa.INTEGER(),
               type_=sa.String(length=32),
               nullable=False)
        batch_op.create_foreign_key(batch_op.f('fk_wishlist_user_id_user'), 'user', ['user_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('wishlist', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_wishlist_user_id_user'), type_='foreignkey')
        batch_op.alter_column('product_id',
               existing_type=sa.String(length=32),
               type_=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('user_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.alter_column('product_route',
               existing_type=sa.String(length=64),
               type_=sa.NUMERIC(precision=64),
               existing_nullable=True)
        batch_op.alter_column('cover_img',
               existing_type=sa.String(length=64),
               type_=sa.NUMERIC(precision=64),
               existing_nullable=True)
        batch_op.drop_column('model')

    with op.batch_alter_table('comment', schema=None) as batch_op:
        batch_op.add_column(sa.Column('code_id', sa.INTEGER(), nullable=True))
        batch_op.drop_constraint(batch_op.f('fk_comment_blog_id_blogs'), type_='foreignkey')
        batch_op.create_foreign_key(None, 'code', ['code_id'], ['id'])
        batch_op.drop_column('author_id')

    # ### end Alembic commands ###

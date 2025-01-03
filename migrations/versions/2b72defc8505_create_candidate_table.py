"""Create candidate table

Revision ID: 2b72defc8505
Revises: fc5958b7aa41
Create Date: 2024-12-03 13:17:29.670105

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2b72defc8505'
down_revision = 'fc5958b7aa41'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('skills', sa.Text(), nullable=True),
    sa.Column('resume_link', sa.String(length=255), nullable=True),
    sa.Column('experience', sa.Text(), nullable=True),
    sa.Column('job_preferences', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('application',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('job_listing_id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=50), nullable=False),
    sa.ForeignKeyConstraint(['candidate_id'], ['candidate.id'], ),
    sa.ForeignKeyConstraint(['job_listing_id'], ['job_listing.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('job_listings')
    op.drop_table('applications')
    op.drop_table('candidates')
    with op.batch_alter_table('job_status_updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('id', sa.Integer(), nullable=False))
        batch_op.add_column(sa.Column('job_listing_id', sa.Integer(), nullable=False))
        batch_op.alter_column('status',
               existing_type=mysql.VARCHAR(length=50),
               type_=sa.String(length=100),
               nullable=False)
        batch_op.drop_constraint('job_status_updates_ibfk_1', type_='foreignkey')
        batch_op.create_foreign_key(None, 'job_listing', ['job_listing_id'], ['id'])
        batch_op.drop_column('status_update_id')
        batch_op.drop_column('job_id')
        batch_op.drop_column('update_date')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('job_status_updates', schema=None) as batch_op:
        batch_op.add_column(sa.Column('update_date', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True))
        batch_op.add_column(sa.Column('job_id', mysql.INTEGER(), autoincrement=False, nullable=True))
        batch_op.add_column(sa.Column('status_update_id', mysql.INTEGER(), autoincrement=True, nullable=False))
        batch_op.drop_constraint(None, type_='foreignkey')
        batch_op.create_foreign_key('job_status_updates_ibfk_1', 'job_listings', ['job_id'], ['id'], ondelete='CASCADE')
        batch_op.alter_column('status',
               existing_type=sa.String(length=100),
               type_=mysql.VARCHAR(length=50),
               nullable=True)
        batch_op.drop_column('job_listing_id')
        batch_op.drop_column('id')

    op.create_table('candidates',
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('skills', mysql.TEXT(), nullable=True),
    sa.Column('resume_link', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('experience', mysql.TEXT(), nullable=True),
    sa.Column('job_preferences', mysql.TEXT(), nullable=True),
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('applications',
    sa.Column('application_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('candidate_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('job_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.VARCHAR(length=50), server_default=sa.text("'Pending'"), nullable=True),
    sa.Column('application_date', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.PrimaryKeyConstraint('application_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('job_listings',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('employer_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('location', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('posted_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('category', mysql.VARCHAR(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.drop_table('application')
    op.drop_table('candidate')
    # ### end Alembic commands ###

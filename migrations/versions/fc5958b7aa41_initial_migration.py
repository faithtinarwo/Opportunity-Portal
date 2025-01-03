"""Initial migration

Revision ID: fc5958b7aa41
Revises: 
Create Date: 2024-12-02 15:08:15.042948

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'fc5958b7aa41'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('candidate',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('resume', sa.String(length=100), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('employer',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('job_listing',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=100), nullable=False),
    sa.Column('description', sa.Text(), nullable=False),
    sa.Column('category', sa.String(length=100), nullable=False),
    sa.Column('employer_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['employer_id'], ['employer.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('status_update',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('status', sa.String(length=100), nullable=False),
    sa.Column('job_listing_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['job_listing_id'], ['job_listing.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('candidates')
    op.drop_table('applications')
    op.drop_table('employers')
    op.drop_table('job_status_updates')
    op.drop_table('job_listings')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('job_listings',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('employer_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('title', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('description', mysql.TEXT(), nullable=True),
    sa.Column('location', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('posted_at', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.Column('category', mysql.VARCHAR(length=100), nullable=False),
    sa.ForeignKeyConstraint(['employer_id'], ['employers.id'], name='job_listings_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('job_status_updates',
    sa.Column('status_update_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('job_id', mysql.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('status', mysql.VARCHAR(length=50), nullable=True),
    sa.Column('update_date', mysql.DATETIME(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    sa.ForeignKeyConstraint(['job_id'], ['job_listings.id'], name='job_status_updates_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('status_update_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('employers',
    sa.Column('id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('industry', mysql.VARCHAR(length=100), nullable=True),
    sa.Column('contact_info', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('location', mysql.VARCHAR(length=255), nullable=True),
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
    sa.ForeignKeyConstraint(['candidate_id'], ['candidates.candidate_id'], name='applications_ibfk_1', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('application_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
    )
    op.create_table('candidates',
    sa.Column('candidate_id', mysql.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('name', mysql.VARCHAR(length=255), nullable=False),
    sa.Column('skills', mysql.TEXT(), nullable=True),
    sa.Column('resume_link', mysql.VARCHAR(length=255), nullable=True),
    sa.Column('experience', mysql.TEXT(), nullable=True),
    sa.Column('job_preferences', mysql.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('candidate_id'),
    mysql_collate='utf8mb4_0900_ai_ci',
    mysql_default_charset='utf8mb4',
    mysql_engine='InnoDB'
)
    # Drop existing tables if they exist
    op.drop_table('status_update', if_exists=True)
    op.drop_table('job_listing', if_exists=True)
    op.drop_table('employer', if_exists=True)
    op.drop_table('candidates', if_exists=True)
    # ### end Alembic commands ###

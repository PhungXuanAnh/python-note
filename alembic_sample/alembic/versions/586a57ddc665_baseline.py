"""baseline

Revision ID: 586a57ddc665
Revises: 
Create Date: 2018-12-14 16:37:35.387378

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '586a57ddc665'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'bug',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('bug_tracker_url', sa.String(), nullable=False),
        sa.Column('root_cause', sa.String()),
        sa.Column('who', sa.String()),
        sa.Column('when', sa.DateTime(), default=sa.func.now())
    )


def downgrade():
    pass

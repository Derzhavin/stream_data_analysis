"""fixed missing foreign key in posts

Revision ID: e20309d4cb61
Revises: 4319019f0f95
Create Date: 2022-11-13 09:41:40.011049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e20309d4cb61'
down_revision = '4319019f0f95'
branch_labels = None
depends_on = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass

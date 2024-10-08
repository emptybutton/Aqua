"""make `glass` not nullable

Revision ID: a4628646fb4a
Revises: f00d68373d9a
Create Date: 2024-06-17 07:29:16.347487

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "a4628646fb4a"
down_revision: Union[str, None] = "f00d68373d9a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "aqua_users", "glass", existing_type=sa.INTEGER(), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "aqua_users", "glass", existing_type=sa.INTEGER(), nullable=True
    )
    # ### end Alembic commands ###

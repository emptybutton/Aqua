"""remove aqua schema

Revision ID: ae957e5f10d9
Revises: 652f294f5cc6
Create Date: 2024-11-04 17:18:20.942028

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision: str = "ae957e5f10d9"
down_revision: Union[str, None] = "652f294f5cc6"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.drop_table("records", schema="aqua")
    op.drop_table("days", schema="aqua")
    op.drop_table("users", schema="aqua")
    op.execute("DROP SCHEMA aqua")


def downgrade() -> None:
    op.execute("CREATE SCHEMA aqua")
    op.create_table(
        "users",
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("target", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("glass", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("weight", sa.INTEGER(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("id", name="aqua_users_pkey"),
        schema="aqua",
    )
    op.create_table(
        "days",
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "water_balance", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("target", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.Column("date_", sa.DATE(), autoincrement=False, nullable=False),
        sa.Column(
            "pinned_result", sa.INTEGER(), autoincrement=False, nullable=True
        ),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "correct_result", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column("result", sa.INTEGER(), autoincrement=False, nullable=False),
        sa.PrimaryKeyConstraint("id", name="days_pkey"),
        schema="aqua",
    )
    op.create_table(
        "records",
        sa.Column(
            "drunk_water", sa.INTEGER(), autoincrement=False, nullable=False
        ),
        sa.Column(
            "recording_time",
            postgresql.TIMESTAMP(timezone=True),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column("user_id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column("id", sa.UUID(), autoincrement=False, nullable=False),
        sa.Column(
            "is_cancelled", sa.BOOLEAN(), autoincrement=False, nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name="records_pkey"),
        schema="aqua",
    )

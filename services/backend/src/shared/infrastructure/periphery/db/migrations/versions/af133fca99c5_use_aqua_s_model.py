"""use `aqua`'s model

Revision ID: af133fca99c5
Revises: da032010791f
Create Date: 2024-10-24 13:18:05.041588

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "af133fca99c5"
down_revision: Union[str, None] = "da032010791f"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    _upgrade_users()
    _upgrade_records()
    _upgrade_days()


class NoDowngradeError(Exception): ...


def downgrade() -> None:
    raise NoDowngradeError


def _upgrade_users() -> None:
    op.alter_column(
        "users",
        "water_balance",
        new_column_name="target",
        schema="aqua",
    )


def _upgrade_records() -> None:
    op.execute("""
        UPDATE aqua.records SET is_accidental = False
        WHERE aqua.records.is_accidental IS NULL
    """)
    op.alter_column(
        "records",
        "is_accidental",
        new_column_name="is_cancelled",
        nullable=False,
        schema="aqua",
    )


def _upgrade_days() -> None:
    op.alter_column(
        "days",
        "real_water_balance",
        new_column_name="water_balance",
        schema="aqua",
    )
    op.alter_column(
        "days",
        "target_water_balance",
        new_column_name="target",
        schema="aqua",
    )
    op.alter_column(
        "days",
        "result",
        new_column_name="pinned_result",
        nullable=True,
        schema="aqua",
    )
    op.execute("""
        UPDATE aqua.days SET pinned_result = NULL
        WHERE NOT aqua.days.is_result_pinned
    """)
    op.drop_column("days", "is_result_pinned", schema="aqua")

"""use access model names

Revision ID: eac8c22edae9
Revises: fc5db45d9b09
Create Date: 2024-10-10 13:07:46.752412

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "eac8c22edae9"
down_revision: Union[str, None] = "fc5db45d9b09"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("users", "accounts", schema="auth")

    op.rename_table(
        "previous_usernames", "previous_account_names", schema="auth"
    )
    op.alter_column(
        "previous_account_names",
        "user_id",
        new_column_name="account_id",
        schema="auth",
    )
    op.alter_column(
        "previous_account_names",
        "username",
        new_column_name="account_name",
        schema="auth",
    )

    op.alter_column(
        "sessions", "user_id", new_column_name="account_id", schema="auth"
    )
    op.alter_column(
        "sessions", "cancelled", new_column_name="is_cancelled", schema="auth"
    )
    op.alter_column(
        "sessions",
        "next_session_id",
        new_column_name="leader_session_id",
        schema="auth",
    )
    op.alter_column(
        "sessions",
        "expiration_date",
        new_column_name="end_time",
        schema="auth",
    )


def downgrade() -> None:
    op.rename_table("accounts", "users", schema="auth")

    op.rename_table(
        "previous_account_names", "previous_usernames", schema="auth"
    )
    op.alter_column(
        "previous_usernames",
        "account_id",
        new_column_name="user_id",
        schema="auth",
    )
    op.alter_column(
        "previous_usernames",
        "account_name",
        new_column_name="username",
        schema="auth",
    )

    op.alter_column(
        "sessions", "account_id", new_column_name="user_id", schema="auth"
    )
    op.alter_column(
        "sessions", "is_cancelled", new_column_name="cancelled", schema="auth"
    )
    op.alter_column(
        "sessions",
        "leader_session_id",
        new_column_name="next_session_id",
        schema="auth",
    )
    op.alter_column(
        "sessions",
        "end_time",
        new_column_name="expiration_date",
        schema="auth",
    )

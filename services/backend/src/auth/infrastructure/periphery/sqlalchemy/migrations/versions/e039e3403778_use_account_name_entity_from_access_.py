"""use account name entity from access model

Revision ID: e039e3403778
Revises: eac8c22edae9
Create Date: 2024-10-10 13:35:49.891971

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "e039e3403778"
down_revision: Union[str, None] = "eac8c22edae9"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "account_names",
        sa.Column("id", sa.Uuid, primary_key=True, nullable=False),
        sa.Column("account_id", sa.Uuid, nullable=False),
        sa.Column("text", sa.String, nullable=False),
        sa.Column("is_current", sa.Boolean, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        schema="auth",
    )
    op.execute("""
        INSERT INTO auth.account_names(id, account_id, text, is_current)
        SELECT gen_random_uuid(), account_id, account_name, false
        FROM (
            SELECT DISTINCT
            auth.previous_account_names.account_id,
            auth.previous_account_names.account_name
            FROM auth.previous_account_names
        )
    """)
    op.execute("""
        UPDATE auth.account_names SET is_current = true
        FROM auth.accounts WHERE auth.account_names.text = auth.accounts.name
    """)
    op.drop_column("accounts", "name", schema="auth")
    op.alter_column(
        "account_names",
        "is_current",
        nullable=False,
        schema="auth",
    )

    op.add_column(
        "previous_account_names",
        sa.Column("account_name_id", sa.Uuid, nullable=True),
        schema="auth",
    )
    op.execute("""
        UPDATE auth.previous_account_names
        SET account_name_id = account_names.id
        FROM auth.account_names
        WHERE (
            auth.previous_account_names.account_id = auth.account_names.account_id
            AND auth.previous_account_names.account_name = auth.account_names.text
        )
    """)  # noqa: E501
    op.alter_column(
        "previous_account_names",
        "account_name_id",
        nullable=False,
        schema="auth",
    )
    op.alter_column(
        "previous_account_names",
        "change_time",
        new_column_name="time",
        schema="auth",
    )
    op.drop_column("previous_account_names", "account_id", schema="auth")
    op.drop_column("previous_account_names", "account_name", schema="auth")
    op.rename_table(
        "previous_account_names", "account_name_taking_times", schema="auth"
    )


def downgrade() -> None:
    op.rename_table(
        "account_name_taking_times", "previous_account_names", schema="auth"
    )
    op.add_column(
        "previous_account_names",
        sa.Column("account_name", sa.String, nullable=True),
        schema="auth",
    )
    op.add_column(
        "previous_account_names",
        sa.Column("account_id", sa.Uuid, nullable=True),
        schema="auth",
    )
    op.alter_column(
        "previous_account_names",
        "time",
        new_column_name="change_time",
        schema="auth",
    )

    op.execute("""
        UPDATE auth.previous_account_names
        SET (
            account_id = auth.account_names.account_id,
            account_name = auth.account_names.text
        )
        FROM auth.account_names
        WHERE (
            auth.previous_account_names.account_name_id = auth.account_names.id
            AND NOT auth.account_names.is_current
        )
    """)

    op.add_column(
        "accounts",
        sa.Column("name", sa.String, nullable=False),
        schema="auth",
    )
    op.execute("""
        UPDATE auth.accounts
        SET name = auth.account_names.text
        FROM auth.account_names
        WHERE (
            auth.account_names.account_id = auth.accounts.id
            AND auth.account_names.is_current
        )
    """)

    op.alter_column(
        "previous_account_names",
        "account_name",
        nullable=False,
        schema="auth",
    )
    op.alter_column(
        "previous_account_names",
        "account_id",
        nullable=False,
        schema="auth",
    )
    op.drop_column("previous_account_names", "account_name_id", schema="auth")
    op.drop_table("account_names", schema="auth")

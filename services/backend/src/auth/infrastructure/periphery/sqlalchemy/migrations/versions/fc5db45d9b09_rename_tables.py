"""rename tables

Revision ID: fc5db45d9b09
Revises: 4bb7a939abd1
Create Date: 2024-10-08 17:49:35.986842

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "fc5db45d9b09"
down_revision: Union[str, None] = "4bb7a939abd1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.rename_table("auth_users", "users", schema="auth")
    op.rename_table(
        "auth_previous_usernames", "previous_usernames", schema="auth"
    )

    op.rename_table("aqua_users", "users", schema="aqua")


def downgrade() -> None:
    op.rename_table("users", "auth_users", schema="auth")
    op.rename_table(
        "previous_usernames", "auth_previous_usernames", schema="auth"
    )

    op.rename_table("users", "aqua_users", schema="aqua")

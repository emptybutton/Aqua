"""use schemas

Revision ID: 4bb7a939abd1
Revises: d3952f9805a1
Create Date: 2024-10-08 13:44:02.236720

"""

from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = "4bb7a939abd1"
down_revision: Union[str, None] = "d3952f9805a1"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE SCHEMA auth")
    op.execute("ALTER TABLE auth_users SET SCHEMA auth")
    op.execute("ALTER TABLE auth_previous_usernames SET SCHEMA auth")
    op.execute("ALTER TABLE sessions SET SCHEMA auth")

    op.execute("CREATE SCHEMA aqua")
    op.execute("ALTER TABLE aqua_users SET SCHEMA aqua")
    op.execute("ALTER TABLE records SET SCHEMA aqua")
    op.execute("ALTER TABLE days SET SCHEMA aqua")


def downgrade() -> None:
    op.execute("ALTER TABLE auth_users SET SCHEMA public")
    op.execute("ALTER TABLE auth_previous_usernames SET SCHEMA public")
    op.execute("ALTER TABLE sessions SET SCHEMA public")

    op.execute("ALTER TABLE aqua_users SET SCHEMA public")
    op.execute("ALTER TABLE records SET SCHEMA public")
    op.execute("ALTER TABLE days SET SCHEMA public")

    op.execute("DROP SCHEMA auth")
    op.execute("DROP SCHEMA aqua")

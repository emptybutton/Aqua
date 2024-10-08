"""add foreign key constraints

Revision ID: 1e0dda32eaaa
Revises: 15b7e9cc6a28
Create Date: 2024-06-18 08:38:52.059096

"""

from typing import Sequence, Union

import sqlalchemy as sa  # noqa: F401
from alembic import op


# revision identifiers, used by Alembic.
revision: str = "1e0dda32eaaa"
down_revision: Union[str, None] = "15b7e9cc6a28"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, "aqua_users", "auth_users", ["id"], ["id"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "aqua_users", type_="foreignkey")  # type: ignore[arg-type]
    # ### end Alembic commands ###

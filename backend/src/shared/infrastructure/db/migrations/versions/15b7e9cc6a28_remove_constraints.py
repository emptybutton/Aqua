"""remove constraints

Revision ID: 15b7e9cc6a28
Revises: a4628646fb4a
Create Date: 2024-06-17 10:10:44.209724

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "15b7e9cc6a28"
down_revision: Union[str, None] = "a4628646fb4a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("aqua_users_id_fkey", "aqua_users", type_="foreignkey")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(
        "aqua_users_id_fkey", "aqua_users", "auth_users", ["id"], ["id"]
    )
    # ### end Alembic commands ###

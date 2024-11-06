from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from auth.application.ports.views import AccountViewFrom
from auth.infrastructure.adapters.repos.db import DBAccounts
from auth.infrastructure.periphery.sqlalchemy import tables


@dataclass(kw_only=True, frozen=True, slots=True)
class DBAccountData:
    account_id: UUID
    account_current_name_text: str


DBAccountView: TypeAlias = DBAccountData | None


class DBAccountViewFrom(AccountViewFrom[DBAccounts, DBAccountView]):
    async def __call__(
        self, db_accounts: DBAccounts, *, account_id: UUID
    ) -> DBAccountView:
        stmt = (
            db_accounts.builder.select(
                tables.account_name_table.c.text.label("current_name_text"),
            )
            .build()
            .where(
                (tables.account_name_table.c.account_id == account_id)
                & tables.account_name_table.c.is_current
            )
            .limit(1)
        )

        result = await db_accounts.connection.execute(stmt)
        row = result.first()

        if row is None:
            return None

        return DBAccountData(
            account_id=account_id,
            account_current_name_text=row.current_name_text,
        )

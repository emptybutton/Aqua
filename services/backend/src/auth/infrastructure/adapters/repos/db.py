from uuid import UUID

from sqlalchemy import exists, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application import ports
from auth.domain.models.access.aggregates.account.root import Account
from shared.infrastructure.periphery.db.stmt_builders import STMTBuilder
from shared.infrastructure.periphery.db.tables import auth as tables


class DBAccounts(ports.repos.Accounts):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__session = connection
        self.__builder = STMTBuilder.for_(connection)

    async def account_with_name(
        self, *, name_text: str
    ) -> Account | None: ...

    async def account_with_id(self, account_id: UUID) -> Account | None: ...

    async def account_with_session(
        self, *, session_id: UUID
    ) -> Account | None:
        ...

    async def contains_account_with_name(self, *, name_text: str) -> bool:
        stmt = self.__builder.select(
            exists(1).where(tables.account_name_table.c.text == name_text)
        ).build()

        return bool(await self.__session.scalar(stmt))

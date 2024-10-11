from copy import copy
from uuid import UUID

from sqlalchemy import exists, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application import ports
from auth.domain.models.access.aggregates.account.root import Account
from shared.infrastructure.periphery.containers import TransactionalContainer
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


class InMemoryAccounts(ports.repos.Accounts, TransactionalContainer[Account]):
    async def account_with_name(
        self, *, name_text: str
    ) -> Account | None:
        for account in self._storage:
            for name in account.names:
                if name.text == name_text:
                    return account

        return None

    async def account_with_id(self, account_id: UUID) -> Account | None:
        for account in self._storage:
            if account.id == account_id:
                return account

        return None

    async def account_with_session(
        self, *, session_id: UUID
    ) -> Account | None:
        for account in self._storage:
            for session in account.sessions:
                if session.id == session_id:
                    return account

        return None

    async def contains_account_with_name(self, *, name_text: str) -> bool:
        account = self.account_with_name(name_text=name_text)

        return account is not None

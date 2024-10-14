from typing import Any, TypeAlias

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application.ports.mappers import AccountMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.db import DBAccounts
from shared.application.ports.mappers import MapperFactory
from shared.infrastructure.periphery.db.tables import auth as tables


_Account: TypeAlias = _account.root.Account
_Values: TypeAlias = list[dict[str, Any]]


class DBAccountMapper(AccountMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, accounts: frozenset[_Account]) -> None:
        stmt = insert(tables.account_table)

        await self.__connection.execute(stmt, self.__values_of(accounts))

    async def update_all(self, accounts: frozenset[_Account]) -> None:
        stmt = (
            update(tables.account_table)
            .where(tables.account_table.c.id == bindparam("id"))
            .values(password_hash=bindparam("password_hash"))
        )

        await self.__connection.execute(stmt, self.__values_of(accounts))

    def __values_of(self, accounts: frozenset[_Account]) -> _Values:
        return [
            dict(id=account.id, password_hash=account.password_hash)
            for account in accounts
        ]


class DBAccountMapperFactory(MapperFactory[DBAccounts, _Account]):
    def __call__(self, db_accounts: DBAccounts) -> DBAccountMapper:
        return DBAccountMapper(db_accounts.connection)

from itertools import chain
from typing import Any, Iterable, TypeAlias
from uuid import uuid4

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application.ports.mappers import AccountNameMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.db import DBAccounts
from shared.application.ports.mappers import MapperFactory
from shared.infrastructure.periphery.db.tables import auth as tables


_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_BecameCurrent: TypeAlias = (
    _account.internal.entities.account_name.BecameCurrent
)

_Values: TypeAlias = list[dict[str, Any]]


class DBAccountNameMapper(AccountNameMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, account_names: frozenset[_AccountName]) -> None:
        if not account_names:
            return

        await self.__insert_to_account_name_table(account_names)
        await self.__insert_to_account_name_taking_time_table(account_names)

    async def update_all(self, account_names: frozenset[_AccountName]) -> None:
        if not account_names:
            return

        await self.__update_account_name_table(account_names)
        await self.__update_account_name_taking_time_table(account_names)

    async def __insert_to_account_name_table(
        self, account_names: frozenset[_AccountName]
    ) -> None:
        stmt = insert(tables.account_name_table)

        values = self.__name_values_of(account_names)
        await self.__connection.execute(stmt, values)

    async def __insert_to_account_name_taking_time_table(
        self, account_names: frozenset[_AccountName]
    ) -> None:
        stmt = insert(tables.account_name_taking_time_table)

        values = self.__time_values_of(account_names)
        await self.__connection.execute(stmt, values)

    async def __update_account_name_table(
        self, account_names: frozenset[_AccountName]
    ) -> None:
        stmt = (
            update(tables.account_name_table)
            .where(tables.account_name_table.c.id == bindparam("id_"))
            .values(
                password_hash=bindparam("password_hash_"),
                text=bindparam("text_"),
                is_current=bindparam("is_current_"),
            )
        )

        values = self.__updating(self.__name_values_of(account_names))
        await self.__connection.execute(stmt, values)

    async def __update_account_name_taking_time_table(
        self, account_names: frozenset[_AccountName]
    ) -> None:
        events = chain.from_iterable(
            account_name.events_with_type(_BecameCurrent)
            for account_name in account_names
        )
        await self.__insert_to_account_name_taking_time_table_by_events(events)

    async def __insert_to_account_name_taking_time_table_by_events(
        self, events: Iterable[_BecameCurrent]
    ) -> None:
        stmt = insert(tables.account_name_taking_time_table)
        await self.__connection.execute(stmt, self.__event_values_of(events))

    def __name_values_of(
        self, account_names: frozenset[_AccountName]
    ) -> _Values:
        return [
            dict(
                id=account_name.id,
                account_id=account_name.account_id,
                text=account_name.text,
                is_current=account_name.is_current,
            )
            for account_name in account_names
        ]

    def __time_values_of(
        self, account_names: frozenset[_AccountName]
    ) -> _Values:
        return [
            dict(
                id=uuid4(),
                account_name_id=account_name.id,
                text=account_name.text,
                time=time.datetime_,
            )
            for account_name in account_names
            for time in account_name.taking_times
        ]

    def __event_values_of(self, events: Iterable[_BecameCurrent]) -> _Values:
        return [
            dict(
                id=uuid4(),
                account_name_id=event.entity.id,
                text=event.entity.text,
                time=event.new_taking_time.datetime_,
            )
            for event in events
        ]

    def __updating(self, values: _Values) -> _Values:
        return [
            {f"{k}_": v for k, v in value.items()}
            for value in values
        ]


class DBAccountNameMapperFactory(MapperFactory[DBAccounts, _AccountName]):
    def __call__(self, db_accounts: DBAccounts) -> DBAccountNameMapper:
        return DBAccountNameMapper(db_accounts.connection)

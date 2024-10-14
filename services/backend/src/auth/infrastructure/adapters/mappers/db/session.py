from typing import Any, TypeAlias

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application.ports.mappers import SessionMapper
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters.repos.db import DBAccounts
from shared.application.ports.mappers import MapperFactory
from shared.infrastructure.periphery.db.tables import auth as tables


_Session: TypeAlias = _account.internal.entities.session.Session

_Value: TypeAlias = dict[str, Any]
_Values: TypeAlias = list[_Value]


class DBSessionMapper(SessionMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, sessions: frozenset[_Session]) -> None:
        stmt = insert(tables.session_table)

        await self.__connection.execute(stmt, self.__values_of(sessions))

    async def update_all(self, sessions: frozenset[_Session]) -> None:
        stmt = (
            update(tables.session_table)
            .where(tables.session_table.c.id == bindparam("id"))
            .values(
                start_time=bindparam("start_time"),
                end_time=bindparam("end_time"),
                is_cancelled=bindparam("is_cancelled"),
                leader_session_id=bindparam("leader_session_id"),
            )
        )

        await self.__connection.execute(stmt, self.__values_of(sessions))

    def __values_of(self, sessions: frozenset[_Session]) -> _Values:
        return list(map(self.__value_of, sessions))

    def __value_of(self, session: _Session) -> _Value:
        start_time = None

        if session.lifetime.start_time:
            start_time = session.lifetime.start_time.datetime_

        return dict(
            id=session.id,
            account_id=session.account_id,
            start_time=start_time,
            end_time=session.lifetime.end_time.datetime_,
            is_cancelled=session.is_cancelled,
            leader_session_id=session.leader_session_id,
        )


class DBAccountMapperFactory(MapperFactory[DBAccounts, _Session]):
    def __call__(self, db_accounts: DBAccounts) -> DBSessionMapper:
        return DBSessionMapper(db_accounts.connection)

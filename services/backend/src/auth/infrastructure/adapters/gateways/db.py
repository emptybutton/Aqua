from typing import Any, TypeAlias
from uuid import UUID

from sqlalchemy import Row, exists, select
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application.ports import gateway as _gateway
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.vos.session_lifetime import SessionLifetime
from auth.domain.models.access.vos.time import Time
from auth.infrastructure.adapters.repos.db import DBAccounts
from auth.infrastructure.periphery.sqlalchemy import tables


_Session: TypeAlias = _account.internal.entities.session.Session


class DBGateway(_gateway.Gateway):
    class Error(Exception): ...

    class UnexpectedDBResult(Error): ...

    def __init__(self, db_accounts: DBAccounts) -> None:
        self.__db_accounts = db_accounts

    @property
    def __connection(self) -> AsyncConnection:
        return self.__db_accounts.connection

    async def session_with_id_and_contains_account_name_with_text(
        self,
        *,
        session_id: UUID,
        account_name_text: str,
    ) -> _gateway.SessionAndPresenceOfAccountNameWithText:
        presence_stmt = select(exists(
            select(1)
            .where(tables.account_name_table.c.text == account_name_text)
            .with_for_update()
        ))
        session_stmt = (
            select(
                tables.session_table.c.account_id,
                tables.session_table.c.start_time,
                tables.session_table.c.end_time,
                tables.session_table.c.is_cancelled,
                tables.session_table.c.leader_session_id,
            )
            .where(tables.session_table.c.id == session_id)
            .with_for_update()
        )

        presence_result = await self.__connection.execute(presence_stmt)
        session_result = await self.__connection.execute(session_stmt)

        session_row = session_result.first()
        presence = bool(presence_result.first())

        return _gateway.SessionAndPresenceOfAccountNameWithText(
            session=self.__session_from(session_row, session_id=session_id),
            contains_account_name_with_text=presence,
        )

    async def session_with_id_and_account_with_name(
        self, *, session_id: UUID, account_name_text: str
    ) -> _gateway.SessionAndAccount:
        account = await self.__db_accounts.account_with_name(
            name_text=account_name_text
        )
        session = await self.session_with_id(session_id)

        return _gateway.SessionAndAccount(session=session, account=account)

    async def session_with_id(self, session_id: UUID) -> _Session | None:
        stmt = (
            select(
                tables.session_table.c.account_id,
                tables.session_table.c.start_time,
                tables.session_table.c.end_time,
                tables.session_table.c.is_cancelled,
                tables.session_table.c.leader_session_id,
            )
            .where(
                tables.session_table.c.id == session_id,
            )
            .limit(1)
            .with_for_update()
        )

        result = await self.__db_accounts.connection.execute(stmt)
        row = result.first()

        return self.__session_from(row, session_id=session_id)

    async def account_with_id_and_contains_account_name_with_text(
        self,
        *,
        account_id: UUID,
        account_name_text: str,
    ) -> _gateway.AccountAndPresenceOfAccountNameWithText:
        account = await self.__db_accounts.account_with_id(account_id)
        contains_account = await self.__db_accounts.contains_account_with_name(
            name_text=account_name_text,
        )

        return _gateway.AccountAndPresenceOfAccountNameWithText(
            account=account,
            contains_account_name_with_text=contains_account,
        )

    def __session_from(
        self, row: Row[Any] | None, *, session_id: UUID
    ) -> _Session | None:
        if row is None:
            return None

        start_time = None

        if row.start_time is not None:
            start_time = Time.with_(datetime_=row.start_time).unwrap()

        lifetime = SessionLifetime(
            start_time=start_time,
            end_time=Time.with_(datetime_=row.end_time).unwrap(),
        )
        return _Session(
            id=session_id,
            account_id=row.account_id,
            lifetime=lifetime,
            is_cancelled=row.is_cancelled,
            leader_session_id=row.leader_session_id,
            events=list(),
        )


class DBGatewayFactory(_gateway.GatewayFactory[DBAccounts]):
    def __call__(self, db_accounts: DBAccounts) -> DBGateway:
        return DBGateway(db_accounts)

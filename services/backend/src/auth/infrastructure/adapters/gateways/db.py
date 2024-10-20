from typing import Any, TypeAlias
from uuid import UUID

from sqlalchemy import Row, exists, select

from auth.application.ports import gateway as _gateway
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.vos.session_lifetime import SessionLifetime
from auth.domain.models.access.vos.time import Time
from auth.infrastructure.adapters.repos.db import DBAccounts
from shared.infrastructure.periphery.db.tables import auth as tables


_Session: TypeAlias = _account.internal.entities.session.Session


class DBGateway(_gateway.Gateway):
    class Error(Exception): ...

    class UnexpectedDBResult(Error): ...

    def __init__(self, db_accounts: DBAccounts) -> None:
        self.__db_accounts = db_accounts

    async def session_with_id_and_contains_account_name_with_text(
        self,
        *,
        session_id: UUID,
        account_name_text: str,
    ) -> _gateway.SessionAndPresenceOfAccountNameWithText:
        substmt = (
            exists(1)
            .where(tables.account_name_table.c.text == account_name_text)
            .label("contains")
        )
        stmt = (
            self.__db_accounts.builder.select(
                substmt,
                tables.session_table.c.account_id,
                tables.session_table.c.start_time,
                tables.session_table.c.end_time,
                tables.session_table.c.is_cancelled,
                tables.session_table.c.leader_session_id,
            )
            .build()
            .outerjoin_from(
                select(1).subquery(),
                tables.session_table,
                tables.session_table.c.id == session_id,
            )
        )

        result = await self.__db_accounts.connection.execute(stmt)
        row = result.first()

        if row is None:
            raise DBGateway.UnexpectedDBResult

        return _gateway.SessionAndPresenceOfAccountNameWithText(
            session=self.__session_from(row, session_id=session_id),
            contains_account_name_with_text=row.contains,
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
            self.__db_accounts.builder.select(
                tables.session_table.c.account_id,
                tables.session_table.c.start_time,
                tables.session_table.c.end_time,
                tables.session_table.c.is_cancelled,
                tables.session_table.c.leader_session_id,
            )
            .build()
            .where(
                tables.session_table.c.id == session_id,
            )
            .limit(1)
        )

        result = await self.__db_accounts.connection.execute(stmt)
        row = result.first()

        if row is None:
            return None

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
        self, row: Row[Any], *, session_id: UUID
    ) -> _Session | None:
        if row.account_id is None:
            return None

        start_time = None

        if row.start_time is not None:
            start_time = Time(datetime_=row.start_time)

        lifetime = SessionLifetime(
            start_time=start_time,
            end_time=Time(datetime_=row.end_time),
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

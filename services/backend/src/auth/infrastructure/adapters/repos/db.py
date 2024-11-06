from typing import TYPE_CHECKING, Any, Iterable, NamedTuple, TypeAlias
from uuid import UUID

from sqlalchemy import Row, Select, exists, select
from sqlalchemy.ext.asyncio import AsyncConnection

from auth.application import ports
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.vos.password import PasswordHash
from auth.domain.models.access.vos.session_lifetime import SessionLifetime
from auth.domain.models.access.vos.time import Time
from auth.infrastructure.periphery.sqlalchemy import tables
from auth.infrastructure.periphery.sqlalchemy.stmt_builders import STMTBuilder


if TYPE_CHECKING:
    from sqlalchemy import NamedFromClause


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


class _CurrentNameItems(NamedTuple):
    current_name: "NamedFromClause"
    current_name_taking_time: "NamedFromClause"


class _PrevousNameItems(NamedTuple):
    prevous_name: "NamedFromClause"
    prevous_name_taking_time: "NamedFromClause"


class _ConstructorItems(NamedTuple):
    stmt: Select[Any]
    current_name_items: _CurrentNameItems
    prevous_name_items: _PrevousNameItems
    session: "NamedFromClause"


class DBAccounts(ports.repos.Accounts):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection
        self.__builder = STMTBuilder(connection)

    @property
    def connection(self) -> AsyncConnection:
        return self.__connection

    @property
    def builder(self) -> STMTBuilder:
        return self.__builder

    @property
    def _stmt_items(self) -> _ConstructorItems:
        session = tables.session_table.alias("session")
        current_name = tables.account_name_table.alias("current_name")
        current_name_taking_time = tables.account_name_taking_time_table.alias(
            "current_name_taking_time"
        )

        prevous_name = tables.account_name_table.alias("prevous_name")
        prevous_name_taking_time = tables.account_name_taking_time_table.alias(
            "prevous_name_taking_time"
        )

        stmt = select(
            tables.account_table.c.id.label("account_id"),
            tables.account_table.c.password_hash.label("account_password_hash"),
            current_name.c.id.label("current_name_id"),
            current_name.c.text.label("current_name_text"),
            current_name_taking_time.c.time.label("current_name_taking_time"),
            prevous_name.c.id.label("prevous_name_id"),
            prevous_name.c.text.label("prevous_name_text"),
            prevous_name_taking_time.c.time.label("prevous_name_taking_time"),
            session.c.id.label("session_id"),
            session.c.start_time.label("session_start_time"),
            session.c.end_time.label("session_end_time"),
            session.c.is_cancelled.label("session_is_cancelled"),
            session.c.leader_session_id.label("leader_session_id"),
        )

        current_name_items = _CurrentNameItems(
            current_name=current_name,
            current_name_taking_time=current_name_taking_time,
        )

        prevous_name_items = _PrevousNameItems(
            prevous_name=prevous_name,
            prevous_name_taking_time=prevous_name_taking_time,
        )

        return _ConstructorItems(
            stmt=stmt,
            session=session,
            current_name_items=current_name_items,
            prevous_name_items=prevous_name_items,
        )

    async def account_with_name(self, *, name_text: str) -> _Account | None:
        name = tables.account_name_table.alias("name")
        stmt, current_name_items, prevous_name_items, session = self._stmt_items
        current_name, current_name_taking_time = current_name_items
        prevous_name, prevous_name_taking_time = prevous_name_items

        stmt = (
            stmt.join_from(
                tables.account_table,
                name,
                (
                    (tables.account_table.c.id == name.c.account_id)
                    & (name.c.text == name_text)
                ),
            )
            .join(
                current_name,
                (
                    (tables.account_table.c.id == current_name.c.account_id)
                    & (current_name.c.is_current)
                ),
            )
            .join(
                current_name_taking_time,
                current_name.c.id == current_name_taking_time.c.account_name_id,
            )
            .outerjoin(
                prevous_name,
                (
                    (tables.account_table.c.id == prevous_name.c.account_id)
                    & (~prevous_name.c.is_current)
                ),
            )
            .outerjoin(
                prevous_name_taking_time,
                prevous_name.c.id == prevous_name_taking_time.c.account_name_id,
            )
            .join(session, tables.account_table.c.id == session.c.account_id)
        )

        return await self.__load_by(stmt)

    async def account_with_id(self, account_id: UUID) -> _Account | None:
        stmt, current_name_items, prevous_name_items, session = self._stmt_items
        current_name, current_name_taking_time = current_name_items
        prevous_name, prevous_name_taking_time = prevous_name_items

        stmt = (
            stmt.join_from(
                tables.account_table,
                current_name,
                (
                    (
                        tables.account_table.c.id
                        == current_name.c.account_id
                        == account_id
                    )
                    & (current_name.c.is_current)
                ),
            )
            .join(
                current_name_taking_time,
                current_name.c.id == current_name_taking_time.c.account_name_id,
            )
            .outerjoin(
                prevous_name,
                (
                    (
                        tables.account_table.c.id
                        == prevous_name.c.account_id
                        == account_id
                    )
                    & (~prevous_name.c.is_current)
                ),
            )
            .outerjoin(
                prevous_name_taking_time,
                prevous_name.c.id == prevous_name_taking_time.c.account_name_id,
            )
            .join(
                session,
                (
                    tables.account_table.c.id
                    == session.c.account_id
                    == account_id
                ),
            )
        )

        return await self.__load_by(stmt)

    async def account_with_session(
        self, *, session_id: UUID
    ) -> _Account | None:
        session_with_id = tables.session_table.alias("session_with_id")
        stmt, current_name_items, prevous_name_items, session = self._stmt_items
        current_name, current_name_taking_time = current_name_items
        prevous_name, prevous_name_taking_time = prevous_name_items

        stmt = (
            stmt.join_from(
                tables.account_table,
                session_with_id,
                (
                    (tables.account_table.c.id == session_with_id.c.account_id)
                    & (session_with_id.c.id == session_id)
                ),
            )
            .join(
                current_name,
                (
                    (tables.account_table.c.id == current_name.c.account_id)
                    & (current_name.c.is_current)
                ),
            )
            .join(
                current_name_taking_time,
                current_name.c.id == current_name_taking_time.c.account_name_id,
            )
            .outerjoin(
                prevous_name,
                (
                    (tables.account_table.c.id == prevous_name.c.account_id)
                    & (~prevous_name.c.is_current)
                ),
            )
            .outerjoin(
                prevous_name_taking_time,
                prevous_name.c.id == prevous_name_taking_time.c.account_name_id,
            )
            .join(session, tables.account_table.c.id == session.c.account_id)
        )

        return await self.__load_by(stmt)

    async def contains_account_with_name(self, *, name_text: str) -> bool:
        stmt = self.__builder.select(
            exists(1).where(tables.account_name_table.c.text == name_text)
        ).build()

        return bool(await self.__connection.scalar(stmt))

    async def __load_by(self, stmt: Select[tuple[Any, ...]]) -> _Account | None:
        result = await self.__connection.execute(stmt)
        rows = result.all()

        return None if len(rows) == 0 else self.__account_from(rows)

    def __account_from(self, rows: Row[Any]) -> _Account | None:
        row = rows[0]

        current_name = self.__current_account_name_from(rows)
        if current_name is None:
            return None

        return _Account(
            id=row.account_id,
            password_hash=PasswordHash(text=row.account_password_hash),
            current_name=current_name,
            previous_names=set(self.__prevous_names_from(rows)),
            sessions=set(self.__sessions_from(rows)),
            events=list(),
        )

    def __sessions_from(self, rows: Row[Any]) -> Iterable[_Session]:
        for row in rows:
            start_time = None

            if row.session_start_time is not None:
                start_time = Time.with_(
                    datetime_=row.session_start_time
                ).unwrap()

            end_time = Time.with_(datetime_=row.session_end_time).unwrap()
            lifetime = SessionLifetime(start_time=start_time, end_time=end_time)
            yield _Session(
                id=row.session_id,
                account_id=row.account_id,
                lifetime=lifetime,
                is_cancelled=row.session_is_cancelled,
                leader_session_id=row.leader_session_id,
                events=list(),
            )

    def __current_account_name_from(
        self, rows: Row[Any]
    ) -> _AccountName | None:
        row = rows[0]
        taking_times = set(self.__current_name_taking_times_from(rows))

        return _AccountName.with_(
            id=row.current_name_id,
            account_id=row.account_id,
            text=row.current_name_text,
            taking_times=taking_times,
            is_current=True,
            events=list(),
        ).unwrap()

    def __current_name_taking_times_from(
        self, rows: Row[Any]
    ) -> Iterable[Time]:
        for row in rows:
            yield Time.with_(datetime_=row.current_name_taking_time).unwrap()

    def __prevous_names_from(self, rows: Row[Any]) -> Iterable[_AccountName]:
        row = rows[0]

        if row.prevous_name_id is None:
            return

        for row in rows:
            taking_times = set(
                self.__prevous_name_taking_times_from(
                    rows, prevous_name_id=row.prevous_name_id
                )
            )

            yield _AccountName.with_(
                id=row.prevous_name_id,
                account_id=row.account_id,
                text=row.prevous_name_text,
                taking_times=taking_times,
                is_current=False,
                events=list(),
            ).unwrap()

    def __prevous_name_taking_times_from(
        self,
        rows: Row[Any],
        *,
        prevous_name_id: UUID,
    ) -> Iterable[Time]:
        for row in rows:
            if row.prevous_name_id == prevous_name_id:
                yield (
                    Time.with_(datetime_=row.prevous_name_taking_time).unwrap()
                )

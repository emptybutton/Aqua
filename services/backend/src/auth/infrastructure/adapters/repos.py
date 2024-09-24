from copy import copy
from uuid import UUID

from sqlalchemy import exists, insert, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.ports import repos
from auth.domain import entities
from auth.domain import value_objects as vos
from shared.infrastructure.periphery import uows
from shared.infrastructure.periphery.db import tables
from shared.infrastructure.periphery.db.stmt_builders import STMTBuilder


class DBUsers(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, user: entities.User) -> None:
        stmt = insert(tables.AuthUser).values(
            id=user.id,
            name=user.name.text,
            password_hash=user.password_hash.text,
        )

        await self.__session.execute(stmt)

    async def find_with_id(self, user_id: UUID) -> entities.User | None:
        query = (
            self.__builder.select(
                tables.AuthUser.name, tables.AuthUser.password_hash
            )
            .build()
            .where(tables.AuthUser.id == user_id)
            .limit(1)
        )
        results = await self.__session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        return entities.User(
            id=user_id,
            name=vos.Username(text=raw_user.name),
            password_hash=vos.PasswordHash(text=raw_user.password_hash),
        )

    async def find_with_name(
        self, username: vos.Username
    ) -> entities.User | None:
        query = (
            self.__builder.select(
                tables.AuthUser.id, tables.AuthUser.password_hash
            )
            .build()
            .where(tables.AuthUser.name == username.text)
            .limit(1)
        )
        results = await self.__session.execute(query)
        raw_user = results.first()

        if raw_user is None:
            return None

        return entities.User(
            id=raw_user.id,
            name=username,
            password_hash=vos.PasswordHash(text=raw_user.password_hash),
        )

    async def contains_with_name(self, username: vos.Username) -> bool:
        query = self.__builder.select(
            exists(1).where(tables.AuthUser.name == username.text)
        ).build()

        return bool(await self.__session.scalar(query))

    async def update(self, user: entities.User) -> None:
        await self.__session.execute(
            update(tables.AuthUser)
            .where(tables.AuthUser.id == user.id)
            .values(
                name=user.name.text,
                password_hash=user.password_hash.text,
            )
        )


class DBSessions(repos.Sessions):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, session: entities.Session) -> None:
        start_time = None

        if session.lifetime.start_time is not None:
            start_time = session.lifetime.start_time.datetime_

        await self.__session.execute(
            insert(tables.Session).values(
                id=session.id,
                user_id=session.user_id,
                start_time=start_time,
                expiration_date=session.lifetime.end_time.datetime_,
                cancelled=session.is_cancelled,
                next_session_id=session.next_session_id,
            )
        )

    async def find_with_id(self, session_id: UUID) -> entities.Session | None:
        query = (
            self.__builder.select(
                tables.Session.user_id,
                tables.Session.start_time,
                tables.Session.expiration_date,
                tables.Session.cancelled,
                tables.Session.next_session_id,
            )
            .build()
            .where(tables.Session.id == session_id)
            .limit(1)
        )

        results = await self.__session.execute(query)
        raw_session = results.first()

        if raw_session is None:
            return None

        start_time = None

        if raw_session.start_time is not None:
            start_time = vos.Time(datetime_=raw_session.start_time)

        lifetime = vos.SessionLifetime(
            start_time=start_time,
            _end_time=vos.Time(datetime_=raw_session.expiration_date),
        )

        return entities.Session(
            id=session_id,
            user_id=raw_session.user_id,
            lifetime=lifetime,
            is_cancelled=raw_session.cancelled or False,
            next_session_id=raw_session.next_session_id,
        )

    async def find_other_with_user_id(
        self, *, current_session_id: UUID, user_id: UUID
    ) -> tuple[entities.Session, ...]:
        stmt = (
            self.__builder.select(
                tables.Session.id,
                tables.Session.start_time,
                tables.Session.expiration_date,
                tables.Session.cancelled,
                tables.Session.next_session_id,
            )
            .build()
            .where(
                (tables.Session.id != current_session_id)
                & (tables.Session.user_id == user_id)
            )
        )

        results = await self.__session.execute(stmt)
        raw_sessions = results.all()

        return tuple(
            entities.Session(
                id=raw_session.id,
                user_id=user_id,
                lifetime=vos.SessionLifetime(
                    start_time=(
                        None
                        if raw_session.start_time is None
                        else vos.Time(datetime_=raw_session.start_time)
                    ),
                    _end_time=vos.Time(datetime_=raw_session.expiration_date),
                ),
                is_cancelled=raw_session.cancelled or False,
                next_session_id=raw_session.next_session_id,
            )
            for raw_session in raw_sessions
        )

    async def update(self, session: entities.Session) -> None:
        start_time = None

        if session.lifetime.start_time is not None:
            start_time = session.lifetime.start_time.datetime_

        await self.__session.execute(
            update(tables.Session)
            .where(tables.Session.id == session.id)
            .values(
                user_id=session.user_id,
                start_time=start_time,
                expiration_date=session.lifetime.end_time.datetime_,
                cancelled=session.is_cancelled,
                next_session_id=session.next_session_id,
            )
        )

    async def update_all(self, sessions: tuple[entities.Session, ...]) -> None:
        stmt = update(tables.Session)

        mapped_sessions = [
            dict(
                id=session.id,
                user_id=session.user_id,
                start_time=(
                    None
                    if session.lifetime.start_time is None
                    else session.lifetime.start_time.datetime_
                ),
                expiration_date=session.lifetime.end_time.datetime_,
                cancelled=session.is_cancelled,
                next_session_id=session.next_session_id,
            )
            for session in sessions
        ]

        options = dict(synchronize_session=None)

        await self.__session.execute(
            stmt,
            mapped_sessions,
            execution_options=options,
        )


class DBPreviousUsernames(repos.PreviousUsernames):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, previous_username: entities.PreviousUsername) -> None:
        change_time = None

        if previous_username.change_time is not None:
            change_time = previous_username.change_time.datetime_

        await self.__session.execute(
            insert(tables.PreviousUsername).values(
                id=previous_username.id,
                user_id=previous_username.user_id,
                username=previous_username.username.text,
                change_time=change_time,
            )
        )

    async def contains_with_username(self, username: vos.Username) -> bool:
        query = self.__builder.select(
            exists(1).where(tables.PreviousUsername.username == username.text)
        ).build()

        return bool(await self.__session.scalar(query))

    async def find_with_username(
        self, username: vos.Username
    ) -> entities.PreviousUsername | None:
        stmt = (
            self.__builder.select(
                tables.PreviousUsername.id,
                tables.PreviousUsername.user_id,
                tables.PreviousUsername.change_time,
            )
            .build()
            .where(
                tables.PreviousUsername.username == username.text,
            )
            .limit(1)
        )

        results = await self.__session.execute(stmt)
        result = results.first()

        if result is None:
            return None

        return entities.PreviousUsername(
            id=result.id,
            user_id=result.user_id,
            username=username,
            change_time=(
                None
                if result.change_time is None
                else vos.Time(datetime_=result.change_time)
            ),
        )


class InMemoryUsers(repos.Users, uows.InMemoryUoW[entities.User]):
    async def add(self, user: entities.User) -> None:
        self._storage.append(copy(user))

    async def find_with_id(self, user_id: UUID) -> entities.User | None:
        for user in self._storage:
            if user.id == user_id:
                return user

        return None

    async def find_with_name(
        self, username: vos.Username
    ) -> entities.User | None:
        for user in self._storage:
            if user.name == username:
                return user

        return None

    async def contains_with_name(self, username: vos.Username) -> bool:
        return any(user.name == username for user in self._storage)

    async def update(self, user: entities.User) -> None:
        for stored_user in tuple(self._storage):
            if user.id == stored_user.id:
                self._storage.remove(stored_user)
                self._storage.append(copy(user))
                break


class InMemorySessions(repos.Sessions, uows.InMemoryUoW[entities.Session]):
    async def add(self, session: entities.Session) -> None:
        self._storage.append(copy(session))

    async def find_with_id(self, session_id: UUID) -> entities.Session | None:
        for session in self._storage:
            if session.id == session_id:
                return session

        return None

    async def find_other_with_user_id(
        self, *, current_session_id: UUID, user_id: UUID
    ) -> tuple[entities.Session, ...]:
        return tuple(
            session
            for session in self._storage
            if session.user_id == user_id and session.id != current_session_id
        )

    async def update(self, session: entities.Session) -> None:
        for stored_session in tuple(self._storage):
            if session.id == stored_session.id:
                self._storage.remove(stored_session)
                self._storage.append(copy(session))
                break

    async def update_all(self, sessions: tuple[entities.Session, ...]) -> None:
        for session in sessions:
            await self.update(session)


class InMemoryPreviousUsernames(
    repos.PreviousUsernames,
    uows.InMemoryUoW[entities.PreviousUsername],
):
    async def add(self, previous_username: entities.PreviousUsername) -> None:
        self._storage.append(copy(previous_username))

    async def contains_with_username(self, username: vos.Username) -> bool:
        for previous_username in self._storage:
            if previous_username.username == username:
                return True

        return False

    async def find_with_username(
        self, username: vos.Username
    ) -> entities.PreviousUsername | None:
        for previous_username in self._storage:
            if previous_username.username == username:
                return previous_username

        return None

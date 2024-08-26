from copy import copy
from uuid import UUID

from sqlalchemy import insert, exists, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.ports import repos
from auth.domain import entities, value_objects as vos
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
                tables.AuthUser.name,
                tables.AuthUser.password_hash,
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
            name=raw_user.name,
            password_hash=vos.PasswordHash(text=raw_user.password_hash),
        )

    async def find_with_name(
        self, username: vos.Username
    ) -> entities.User | None:
        query = (
            self.__builder.select(
                tables.AuthUser.id,
                tables.AuthUser.password_hash,
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


class DBSessions(repos.Sessions):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session
        self.__builder = STMTBuilder.of(session)

    async def add(self, session: entities.Session) -> None:
        await self.__session.execute(
            insert(tables.Session).values(
                id=session.id,
                user_id=session.user_id,
                start_time=session.lifetime.start_time,
                expiration_date=session.lifetime.end_time,
            )
        )

    async def find_with_id(self, session_id: UUID) -> entities.Session | None:
        query = (
            self.__builder.select(
                tables.Session.user_id,
                tables.Session.start_time,
                tables.Session.expiration_date,
            )
            .build()
            .where(tables.Session.id == session_id)
            .limit(1)
        )

        results = await self.__session.execute(query)
        raw_session = results.first()

        if raw_session is None:
            return None

        lifetime = vos.SessionLifetime(
            _start_time=raw_session.start_time,
            _end_time=raw_session.expiration_date,
        )

        return entities.Session(
            id=session_id,
            user_id=raw_session.user_id,
            lifetime=lifetime,
        )

    async def update(self, session: entities.Session) -> None:
        await self.__session.execute(
            update(tables.Session)
            .where(tables.Session.id == session.id)
            .values(
                user_id=session.user_id,
                start_time=session.lifetime.start_time,
                expiration_date=session.lifetime.end_time,
            )
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

    async def contains_with_name(
        self,
        username: vos.Username,
    ) -> bool:
        return any(user.name == username for user in self._storage)


class InMemorySessions(repos.Sessions, uows.InMemoryUoW[entities.Session]):
    async def add(self, session: entities.Session) -> None:
        self._storage.append(copy(session))

    async def find_with_id(self, session_id: UUID) -> entities.Session | None:
        for session in self._storage:
            if session.id == session_id:
                return session

        return None

    async def update(self, session: entities.Session) -> None:
        for stored_session in self._storage:
            if session.id == stored_session.id:
                self._storage.remove(stored_session)
                self._storage.append(copy(session))
                break

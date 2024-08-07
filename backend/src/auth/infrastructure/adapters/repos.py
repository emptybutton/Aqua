from uuid import UUID

from sqlalchemy import insert, exists
from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.ports import repos
from auth.domain import entities, value_objects as vos
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

    async def find_with_id(
        self, user_id: UUID
    ) -> entities.User | None:
        query = (
            self.__builder
            .select(
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
            self.__builder
            .select(
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
        query = (
            self.__builder
            .select(exists(1).where(tables.AuthUser.name == username.text))
            .build()
        )

        return bool(await self.__session.scalar(query))

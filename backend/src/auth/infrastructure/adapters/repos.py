from typing import Optional, Any
from uuid import UUID

from sqlalchemy import select, insert, exists
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.ports import repos
from src.auth.domain import entities, value_objects
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, session: AsyncSession) -> None:
        self.__session = session

    async def add(self, user: entities.User) -> None:
        stmt = insert(tables.AuthUser).values(
            id=user.id,
            name=user.name.text,
            password_hash=user.password_hash.text,
        )

        await self.__session.execute(stmt)

    async def get_by_id(
        self, user_id: UUID
    ) -> Optional[entities.User]:
        query = (
            select(
                tables.AuthUser.id,
                tables.AuthUser.name,
                tables.AuthUser.password_hash,
            )
            .where(tables.AuthUser.id == user_id)
            .limit(1)
        )
        results = await self.__session.execute(query)

        return self.__user_from(results.first())

    async def get_by_name(
        self, username: value_objects.Username
    ) -> Optional[entities.User]:
        query = (
            select(
                tables.AuthUser.id,
                tables.AuthUser.name,
                tables.AuthUser.password_hash,
            )
            .where(tables.AuthUser.name == username.text)
            .limit(1)
        )
        results = await self.__session.execute(query)

        return self.__user_from(results.first())

    async def has_with_name(self, username: value_objects.Username) -> bool:
        query = select(exists(1).where(tables.AuthUser.name == username.text))

        return bool(await self.__session.scalar(query))

    def __user_from(self, row_user: Any) -> Optional[entities.User]:  # noqa: ANN401
        if row_user is None:
            return None

        return entities.User(
            id=row_user.id,
            name=value_objects.Username(row_user.name),
            password_hash=value_objects.PasswordHash(row_user.password_hash),
        )

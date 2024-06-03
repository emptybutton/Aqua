from typing import Optional

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.application.ports import repos
from src.auth.domain import entities, value_objects
from src.shared.infrastructure.db import tables


class Users(repos.Users):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add(self, user: entities.User) -> None:
        stmt = insert(tables.AuthUser).values(
            id=user.id,
            name=user.name.text,
            password_hash=user.password_hash.text,
        )

        await self.__connection.execute(stmt)

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
        )
        results = await self.__connection.execute(query)
        row_user = results.first()

        if row_user is None:
            return None

        return entities.User(
            id=row_user.id,
            name=value_objects.Username(row_user.name),
            password_hash=value_objects.PasswordHash(row_user.password_hash),
        )

    async def has_with_name(self, username: value_objects.Username) -> bool:
        query = (
            select(tables.AuthUser)
            .where(tables.AuthUser.name == username.text)
            .exists()
        )

        result: bool = await self.__connection.execute(query).scalar()  # type: ignore[call-overload]
        return result

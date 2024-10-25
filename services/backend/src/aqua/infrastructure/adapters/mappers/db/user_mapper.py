from typing import Iterable

from sqlalchemy import bindparam, insert, update
from sqlalchemy.ext.asyncio import AsyncConnection

from aqua.application.ports.mappers import UserMapper, UserMapperTo
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.repos.db.users import DBUsers
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    glass_value_of,
    maybe_weight_value_of,
    target_value_of,
)
from aqua.infrastructure.periphery.sqlalchemy.values import Value, updating
from shared.infrastructure.periphery.db.tables import aqua as tables


class DBUserMapper(UserMapper):
    def __init__(self, connection: AsyncConnection) -> None:
        self.__connection = connection

    async def add_all(self, users: Iterable[User]) -> None:
        users = frozenset(users)

        if not users:
            return

        stmt = insert(tables.user_table)

        values = list(map(self.__value_of, users))
        await self.__connection.execute(stmt, values)

    async def update_all(self, users: Iterable[User]) -> None:
        users = frozenset(users)

        if not users:
            return

        stmt = (
            update(tables.user_table)
            .where(tables.user_table.c.id == bindparam("id_"))
            .values(
                target=bindparam("target_"),
                glass=bindparam("glass_"),
                weight=bindparam("weight_"),
            )
        )

        values = list(map(self.__value_of, users))
        await self.__connection.execute(stmt, updating(values))

    def __value_of(self, user: User) -> Value:
        return dict(
            id=user.id,
            target=target_value_of(user.target),
            glass=glass_value_of(user.glass),
            weight=maybe_weight_value_of(user.weight),
        )


class DBUserMapperTo(UserMapperTo[DBUsers]):
    def __call__(self, db_users: DBUsers) -> DBUserMapper:
        return DBUserMapper(db_users.connection)

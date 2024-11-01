from typing import Iterable

from pymongo import AsyncClientSession

from aqua.application.ports.mappers import UserMapper, UserMapperTo
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.repos.in_memory.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import execute, to_put
from aqua.infrastructure.periphery.serializing.from_model.to_table_attribute import (  # noqa: E501
    glass_value_of,
    maybe_weight_value_of,
    target_value_of,
)


class MongoUserMapper(UserMapper):
    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, users: Iterable[User]) -> None:
        await self.__put(users)

    async def update_all(self, users: Iterable[User]) -> None:
        await self.__put(users)

    async def __put(self, users: Iterable[User]) -> None:
        operations = (to_put(self.__document_of(user)) for user in users)

        await execute(
            operations,
            session=self.__session,
            comment="put users",
            namespace="db.users",
        )

    def __document_of(self, user: User) -> Document:
        return {
            "_id": user.id,
            "target": target_value_of(user.target),
            "glass": glass_value_of(user.glass),
            "weight": maybe_weight_value_of(user.weight),
        }


class MongoUserMapperTo(UserMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoUserMapper:
        return MongoUserMapper(mongo_users.session)

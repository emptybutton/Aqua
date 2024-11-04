from typing import Iterable

from pymongo.asynchronous.client_session import AsyncClientSession

from aqua.application.ports.mappers import UserMapper, UserMapperTo
from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.pymongo.operations import (
    RootOperations,
    execute,
)
from aqua.infrastructure.periphery.serializing.from_model.to_document import (
    document_glass_of,
    document_target_of,
    maybe_document_weight_of,
)


class MongoUserMapper(UserMapper):
    __operations = RootOperations(namespace="db.users")

    def __init__(self, session: AsyncClientSession) -> None:
        self.__session = session

    async def add_all(self, users: Iterable[User]) -> None:
        await self.__put(users)

    async def update_all(self, users: Iterable[User]) -> None:
        await self.__put(users)

    async def __put(self, users: Iterable[User]) -> None:
        operations = (
            self.__operations.to_put(self.__document_of(user)) for user in users
        )

        await execute(operations, session=self.__session, comment="put users")

    def __document_of(self, user: User) -> Document:
        return {
            "_id": user.id,
            "target": document_target_of(user.target),
            "glass": document_glass_of(user.glass),
            "weight": maybe_document_weight_of(user.weight),
        }


class MongoUserMapperTo(UserMapperTo[MongoUsers]):
    def __call__(self, mongo_users: MongoUsers) -> MongoUserMapper:
        return MongoUserMapper(mongo_users.session)

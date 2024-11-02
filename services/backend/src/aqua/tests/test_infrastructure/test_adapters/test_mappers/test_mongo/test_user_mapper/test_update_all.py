from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.primitives.vos.water import Water
from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_mutated_user1(  # noqa: PLR0917
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user1: User,
    user_documents: list[Document],
    user_mapper: MongoUserMapper,
) -> None:
    user1.glass = Glass(capacity=Water.with_(milliliters=5_000_000).unwrap())

    await user_mapper.update_all([user1])

    user_documents[0]["glass"] = 5_000_000

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents


async def test_without_users(
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user_documents: list[Document],
    user_mapper: MongoUserMapper,
) -> None:
    await user_mapper.update_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

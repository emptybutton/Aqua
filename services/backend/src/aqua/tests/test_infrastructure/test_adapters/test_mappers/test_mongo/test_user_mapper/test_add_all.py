from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.root import User
from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_users(  # noqa: PLR0917
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    users: list[User],
    user_documents: list[Document],
    user_mapper: MongoUserMapper,
) -> None:
    await user_mapper.add_all(users)

    for user_document in user_documents:
        del user_document["records"]
        del user_document["days"]

    async_documents = mongo_client.db.users.find({}, session=mongo_session)
    added_documents = [document async for document in async_documents]

    assert user_documents == added_documents


async def test_without_users(
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user_documents: list[Document],
    user_mapper: MongoUserMapper,
) -> None:
    await user_mapper.add_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

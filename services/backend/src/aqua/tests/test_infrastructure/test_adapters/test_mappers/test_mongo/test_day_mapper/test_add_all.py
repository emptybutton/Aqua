from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_user2_days(  # noqa: PLR0917
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user2_days: list[Day],
    user2_document: Document,
    day_mapper: MongoDayMapper,
) -> None:
    await day_mapper.add_all(user2_days)

    del user2_document["records"]
    del user2_document["target"]
    del user2_document["glass"]
    del user2_document["weight"]

    async_documents = mongo_client.db.users.find({}, session=mongo_session)
    stored_documents = [document async for document in async_documents]

    assert [user2_document] == stored_documents


async def test_without_users(
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user_documents: list[Document],
    day_mapper: MongoDayMapper,
) -> None:
    await day_mapper.add_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

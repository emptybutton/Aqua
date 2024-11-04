from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_user2_records(  # noqa: PLR0917
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user2_records: list[Record],
    user2_document: Document,
    record_mapper: MongoRecordMapper,
) -> None:
    await record_mapper.add_all(user2_records)

    del user2_document["days"]
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
    record_mapper: MongoRecordMapper,
) -> None:
    await record_mapper.add_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

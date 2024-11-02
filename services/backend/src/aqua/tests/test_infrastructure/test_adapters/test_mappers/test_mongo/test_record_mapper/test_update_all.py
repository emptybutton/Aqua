from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_user2_record3(  # noqa: PLR0917
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user2_record2: Record,
    user_documents: list[Document],
    record_mapper: MongoRecordMapper,
) -> None:
    user2_record2.drunk_water = Water.with_(milliliters=5_000_000).unwrap()

    await record_mapper.update_all([user2_record2])

    user_documents[1]["records"][1]["drunk_water"] = 5_000_000

    async_documents = mongo_client.db.users.find({}, session=mongo_session)
    stored_documents = [document async for document in async_documents]

    assert user_documents == stored_documents


async def test_without_users(
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user_documents: list[Document],
    record_mapper: MongoRecordMapper,
) -> None:
    await record_mapper.update_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

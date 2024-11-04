from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapper,
)
from aqua.infrastructure.periphery.pymongo.document import Document


async def test_with_user2_day2(  # noqa: PLR0917
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user2_day2: Day,
    user_documents: list[Document],
    day_mapper: MongoDayMapper,
) -> None:
    user2_day2.target = Target(
        water_balance=WaterBalance(
            water=Water.with_(milliliters=5_000_000).unwrap()
        )
    )

    await day_mapper.update_all([user2_day2])

    user_documents[1]["days"][1]["target"] = 5_000_000

    async_documents = mongo_client.db.users.find({}, session=mongo_session)
    stored_documents = [document async for document in async_documents]

    assert user_documents == stored_documents


async def test_without_users(
    full_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    user_documents: list[Document],
    day_mapper: MongoDayMapper,
) -> None:
    await day_mapper.update_all([])

    async_db_documents = mongo_client.db.users.find({}, session=mongo_session)
    db_documents = [document async for document in async_db_documents]

    assert user_documents == db_documents

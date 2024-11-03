from uuid import UUID

from pymongo import AsyncMongoClient
from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture, raises

from aqua.infrastructure.adapters.transactions.mongo.transaction import (
    MongoTransaction,
)
from aqua.infrastructure.periphery.pymongo.document import Document


@fixture
def transaction(mongo_session: AsyncMongoSession) -> MongoTransaction:
    return MongoTransaction(mongo_session)


async def test_positive_case(
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    transaction: MongoTransaction,
) -> None:
    document = {"_id": UUID(int=0), "x": 4}

    async with transaction:
        await mongo_client.db.users.insert_one(document, session=mongo_session)

    results = await mongo_client.db.users.find(session=mongo_session).to_list()
    assert [document] == results


class NegativeCaseError(Exception): ...


async def test_negative_case(
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    transaction: MongoTransaction,
) -> None:
    document = {"_id": UUID(int=0), "x": 4}
    await mongo_client.db.users.insert_one(document, session=mongo_session)

    with raises(NegativeCaseError):
        async with transaction:
            await mongo_client.db.users.update_one(
                {"_id": UUID(int=0)},
                {"$set": {"x": 5}},
                session=mongo_session,
            )
            raise NegativeCaseError

    results = await mongo_client.db.users.find(session=mongo_session).to_list()
    assert [document] == results


async def test_rollback(
    empty_mongo: None,  # noqa: ARG001
    mongo_client: AsyncMongoClient[Document],
    mongo_session: AsyncMongoSession,
    transaction: MongoTransaction,
) -> None:
    document = {"_id": UUID(int=0), "x": 4}
    await mongo_client.db.users.insert_one(document, session=mongo_session)

    async with transaction:
        await mongo_client.db.users.update_one(
            {"_id": UUID(int=0)},
            {"$set": {"x": 5}},
            session=mongo_session,
        )
        await transaction.rollback()

    results = await mongo_client.db.users.find(session=mongo_session).to_list()
    assert [document] == results

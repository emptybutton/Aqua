from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.mappers.mongo.day_mapper import (
    MongoDayMapper,
)


@fixture
def day_mapper(mongo_session: AsyncMongoSession) -> MongoDayMapper:
    return MongoDayMapper(mongo_session)

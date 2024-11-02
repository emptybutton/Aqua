from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.mappers.mongo.record_mapper import (
    MongoRecordMapper,
)


@fixture
def day_mapper(mongo_session: AsyncMongoSession) -> MongoRecordMapper:
    return MongoRecordMapper(mongo_session)

from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.mappers.mongo.user_mapper import (
    MongoUserMapper,
)


@fixture
def user_mapper(mongo_session: AsyncMongoSession) -> MongoUserMapper:
    return MongoUserMapper(mongo_session)

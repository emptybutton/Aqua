from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.repos.mongo.users import MongoUsers


@fixture
def mongo_users(mongo_session: AsyncMongoSession) -> MongoUsers:
    return MongoUsers(mongo_session)

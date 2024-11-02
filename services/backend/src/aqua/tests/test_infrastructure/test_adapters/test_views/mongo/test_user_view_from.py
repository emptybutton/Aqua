from datetime import date
from uuid import UUID

from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.repos.mongo.users import (
    MongoUsers,
)
from aqua.infrastructure.adapters.views.mongo.user_view_from import (
    DBUserViewFromMongoUsers,
)
from aqua.infrastructure.periphery.views.db.user_view import DBUserViewData


@fixture
def user_view_from() -> DBUserViewFromMongoUsers:
    return DBUserViewFromMongoUsers()


async def test_with_user2_on_day1(
    full_mongo: None,  # noqa: ARG001
    user_view_from: DBUserViewFromMongoUsers,
    mongo_session: AsyncMongoSession,
    user2_db_view_on_day1: DBUserViewData,
) -> None:
    result_view = await user_view_from(
        MongoUsers(mongo_session),
        user_id=UUID(int=2),
        date_=date(2000, 1, 1),
    )

    assert result_view == user2_db_view_on_day1


async def test_without_user(
    empty_mongo: None,  # noqa: ARG001
    user_view_from: DBUserViewFromMongoUsers,
    mongo_session: AsyncMongoSession,
) -> None:
    user_id = UUID(int=0)
    date_ = date(2006, 1, 1)

    result_view = await user_view_from(
        MongoUsers(mongo_session), user_id=user_id, date_=date_
    )

    assert result_view is None

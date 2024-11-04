from datetime import date
from uuid import UUID

from pymongo.asynchronous.client_session import (
    AsyncClientSession as AsyncMongoSession,
)
from pytest import fixture

from aqua.infrastructure.adapters.repos.mongo.users import (
    MongoUsers,
)
from aqua.infrastructure.adapters.views.mongo.day_view_from import (
    DBDayViewFromMongoUsers,
)
from aqua.infrastructure.periphery.views.db.day_view import (
    DBDayView,
    empty_db_day_view_with,
)


@fixture
def day_view_from() -> DBDayViewFromMongoUsers:
    return DBDayViewFromMongoUsers()


async def test_with_user2_day1(
    full_mongo: None,  # noqa: ARG001
    day_view_from: DBDayViewFromMongoUsers,
    mongo_session: AsyncMongoSession,
    user2_day1_db_view: DBDayView,
) -> None:
    result_view = await day_view_from(
        MongoUsers(mongo_session),
        user_id=UUID(int=2),
        date_=date(2000, 1, 1),
    )

    assert result_view == user2_day1_db_view


async def test_without_user(
    empty_mongo: None,  # noqa: ARG001
    day_view_from: DBDayViewFromMongoUsers,
    mongo_session: AsyncMongoSession,
) -> None:
    user_id = UUID(int=0)
    date_ = date(2006, 1, 1)

    result_view = await day_view_from(
        MongoUsers(mongo_session), user_id=user_id, date_=date_
    )

    assert result_view == empty_db_day_view_with(user_id=user_id, date_=date_)

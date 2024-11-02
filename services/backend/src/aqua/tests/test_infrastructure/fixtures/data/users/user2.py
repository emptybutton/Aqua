from datetime import UTC, date, datetime
from uuid import UUID

from pytest import fixture

from aqua.domain.framework.entity import Entities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.periphery.pymongo.document import Document
from aqua.infrastructure.periphery.views.db.day_view import (
    DBDayView,
    DBDayViewRecordData,
)
from aqua.infrastructure.periphery.views.db.user_view import (
    DBUserViewData,
    DBUserViewRecordData,
)


@fixture
def user2_day1() -> Day:
    return Day(
        id=UUID(int=1),
        events=list(),
        user_id=UUID(int=1),
        date_=date(2000, 1, 1),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=500).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=200).unwrap()),
        pinned_result=None,
    )


@fixture
def user2_day2() -> Day:
    return Day(
        id=UUID(int=2),
        events=list(),
        user_id=UUID(int=1),
        date_=date(2000, 1, 5),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=50_000).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=100).unwrap()),
        pinned_result=Result.good,
    )


@fixture
def user2_days(user2_day1: Day, user2_day2: Day) -> list[Day]:
    return [user2_day1, user2_day2]


@fixture
def user2_record1() -> Record:
    return Record(
        id=UUID(int=1),
        events=list(),
        user_id=UUID(int=2),
        drunk_water=Water.with_(milliliters=100).unwrap(),
        recording_time=(
            Time.with_(
                datetime_=datetime(2000, 1, 5, 20, 15, tzinfo=UTC)
            ).unwrap()
        ),
        is_cancelled=False,
    )


@fixture
def user2_record2() -> Record:
    return Record(
        id=UUID(int=2),
        events=list(),
        user_id=UUID(int=2),
        drunk_water=Water.with_(milliliters=100_000).unwrap(),
        recording_time=(
            Time.with_(
                datetime_=datetime(2000, 1, 1, 16, 00, tzinfo=UTC)
            ).unwrap()
        ),
        is_cancelled=True,
    )


@fixture
def user2_record3() -> Record:
    return Record(
        id=UUID(int=3),
        events=list(),
        user_id=UUID(int=2),
        drunk_water=Water.with_(milliliters=290).unwrap(),
        recording_time=(
            Time.with_(
                datetime_=datetime(2000, 1, 1, 15, 30, tzinfo=UTC)
            ).unwrap()
        ),
        is_cancelled=False,
    )


@fixture
def user2_record4() -> Record:
    return Record(
        id=UUID(int=4),
        events=list(),
        user_id=UUID(int=2),
        drunk_water=Water.with_(milliliters=210).unwrap(),
        recording_time=(
            Time.with_(
                datetime_=datetime(2000, 1, 1, 10, 30, tzinfo=UTC)
            ).unwrap()
        ),
        is_cancelled=False,
    )


@fixture
def user2_records(
    user2_record1: Record,
    user2_record2: Record,
    user2_record3: Record,
    user2_record4: Record,
) -> list[Record]:
    return [user2_record1, user2_record2, user2_record3, user2_record4]


@fixture
def user2(user2_days: list[Day], user2_records: list[Record]) -> User:
    return User(
        id=UUID(int=2),
        events=list(),
        target=Target(water_balance=WaterBalance(
            water=Water.with_(milliliters=50_000).unwrap()
        )),
        glass=Glass(capacity=Water.with_(milliliters=500).unwrap()),
        weight=Weight.with_(kilograms=75).unwrap(),
        days=Entities(user2_days),
        records=Entities(user2_records),
    )


@fixture
def user2_document() -> Document:
    return {
        "_id": UUID(int=2),
        "target": 50_000,
        "glass": 500,
        "weight": 75,
        "days": [
            {
                "_id": UUID(int=1),
                "date": datetime(2000, 1, 1),
                "target": 2000,
                "water_balance": 500,
                "result": 2,
                "correct_result": 2,
                "pinned_result": None,
            },
            {
                "_id": UUID(int=2),
                "date": datetime(2000, 1, 5),
                "target": 50_000,
                "water_balance": 100,
                "result": 1,
                "correct_result": 2,
                "pinned_result": 1,
            }
        ],
        "records": [
            {
                "_id": UUID(int=1),
                "drunk_water": 100,
                "recording_time": datetime(2000, 1, 5, 20, 15, tzinfo=UTC),
                "is_cancelled": False,
            },
            {
                "_id": UUID(int=2),
                "drunk_water": 100_000,
                "recording_time": datetime(2000, 1, 1, 16, 00, tzinfo=UTC),
                "is_cancelled": True,
            },
            {
                "_id": UUID(int=3),
                "drunk_water": 290,
                "recording_time": datetime(2000, 1, 1, 15, 30, tzinfo=UTC),
                "is_cancelled": False,
            },
            {
                "_id": UUID(int=4),
                "drunk_water": 210,
                "recording_time": datetime(2000, 1, 1, 10, 30, tzinfo=UTC),
                "is_cancelled": False,
            },
        ],
    }


@fixture
def user2_db_view_on_day1() -> DBUserViewData:
    record3_view = DBUserViewRecordData(
        record_id=UUID(int=3),
        drunk_water_milliliters=290,
        recording_time=datetime(2000, 1, 1, 15, 30, tzinfo=UTC),
    )

    record4_view = DBUserViewRecordData(
        record_id=UUID(int=4),
        drunk_water_milliliters=210,
        recording_time=datetime(2000, 1, 1, 10, 30, tzinfo=UTC),
    )

    return DBUserViewData(
        user_id=UUID(int=1),
        glass_milliliters=500,
        weight_kilograms=75,
        date_=date(2000, 1, 1),
        target_water_balance_milliliters=2000,
        water_balance_milliliters=500,
        result_code=2,
        correct_result_code=2,
        pinned_result_code=None,
        records=(record3_view, record4_view)
    )


@fixture
def day1_db_view() -> DBDayView:
    record3_view = DBDayViewRecordData(
        record_id=UUID(int=3),
        drunk_water_milliliters=290,
        recording_time=datetime(2000, 1, 1, 15, 30, tzinfo=UTC),
    )

    record4_view = DBDayViewRecordData(
        record_id=UUID(int=4),
        drunk_water_milliliters=210,
        recording_time=datetime(2000, 1, 1, 10, 30, tzinfo=UTC),
    )

    return DBDayView(
        user_id=UUID(int=1),
        date_=date(2000, 1, 1),
        target_water_balance_milliliters=2000,
        water_balance_milliliters=500,
        result_code=2,
        correct_result_code=2,
        pinned_result_code=None,
        records=(record3_view, record4_view)
    )

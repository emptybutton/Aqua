from datetime import UTC, datetime

from dirty_equals import IsNow
from pytest import mark

from aqua.domain.framework.entity import FrozenEntities
from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.target import Result
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.water import (
    Water,
)
from aqua.infrastructure.periphery.logs.in_memory_logs import (
    NewDayLog,
    NewRecordLog,
)
from aqua.tests.test_application.test_cases.test_write_water.conftest import (
    Context,
)


@mark.asyncio
async def test_result(context_with_user2: Context, user2: User) -> None:
    view = (await context_with_user2.write_water(user2.id, None)).unwrap()

    water = Water.with_(milliliters=300).unwrap()
    assert view.new_record.user_id == user2.id
    assert view.new_record.drunk_water == water
    assert view.new_record.recording_time.datetime_ == IsNow(tz=UTC)
    assert view.previous_records == tuple()
    assert view.day.user_id == user2.id
    assert view.day.date_ == datetime.now(UTC).date()
    assert view.day.target == user2.target
    assert view.day.water_balance == WaterBalance(water=water)
    assert view.day.result is Result.not_enough_water
    assert not view.day.is_result_pinned


@mark.asyncio
async def test_storage(context_with_user2: Context, user2: User) -> None:
    context = context_with_user2

    view = (await context_with_user2.write_water(user2.id, None)).unwrap()

    users = FrozenEntities([view.user.without_aggregation()])
    days = FrozenEntities([view.day])
    records = FrozenEntities([view.new_record])

    assert context.users.storage.users.without_aggregation() == users
    assert context.users.storage.days == days
    assert context.users.storage.records == records


@mark.asyncio
async def test_logs(context_with_user2: Context, user2: User) -> None:
    context = context_with_user2

    view = (await context.write_water(user2.id, None)).unwrap()

    new_day_log = NewDayLog(day=view.day)
    new_record_log = NewRecordLog(record=view.new_record)

    assert context.logger.registred_user_logs == tuple()
    assert context.logger.registered_user_registration_logs == tuple()
    assert context.logger.record_without_day_logs == tuple()
    assert context.logger.new_day_logs == (new_day_log,)
    assert context.logger.new_day_state_logs == tuple()
    assert context.logger.new_record_logs == (new_record_log,)
    assert context.logger.record_cancellation_logs == tuple()

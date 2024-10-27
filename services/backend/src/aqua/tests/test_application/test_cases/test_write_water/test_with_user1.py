from datetime import UTC

from dirty_equals import IsNow
from pytest import mark

from aqua.domain.framework.entity import FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.target import Result
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.water import (
    Water,
)
from aqua.infrastructure.periphery.logs.in_memory_logs import (
    NewDayStateLog,
    NewRecordLog,
)
from aqua.tests.test_application.test_cases.test_write_water.conftest import (
    Context,
)


@mark.asyncio
async def test_result(
    context_with_user1: Context,
    user1: User,
    user1_day2: Day,
    user1_day2_record1: Record,
    user1_day2_record2: Record,
) -> None:
    context = context_with_user1
    drunk_water = Water.with_(milliliters=300).unwrap()

    view = (await context.write_water(user1.id, None)).unwrap()

    assert view.new_record.user_id == user1.id
    assert view.new_record.drunk_water == drunk_water
    assert view.new_record.recording_time.datetime_ == IsNow(tz=UTC)
    assert view.previous_records == (user1_day2_record2, user1_day2_record1)
    assert view.user.without_aggregation() == user1.without_aggregation()
    assert view.day.user_id == user1_day2.user_id
    assert view.day.date_ == user1_day2.date_
    assert view.day.target == user1_day2.target
    assert view.day.water_balance == WaterBalance(
        water=Water.with_(milliliters=950).unwrap()
    )
    assert view.day.result is Result.good
    assert not view.day.is_result_pinned


@mark.asyncio
async def test_storage(  # noqa: PLR0917
    context_with_user1: Context,
    user1: User,
    user1_day1: Day,
    user1_day1_record1: Record,
    user1_day2_record1: Record,
    user1_day2_record2: Record,
) -> None:
    context = context_with_user1

    view = (await context.write_water(user1.id, None)).unwrap()

    users = FrozenEntities([view.user.without_aggregation()])
    days = FrozenEntities([view.day, user1_day1])
    records = FrozenEntities([
        user1_day1_record1,
        user1_day2_record2,
        user1_day2_record1,
        view.new_record,
    ])

    assert context.users.storage.users.without_aggregation() == users
    assert context.users.storage.days == days
    assert context.users.storage.records == records


@mark.asyncio
async def test_logs(context_with_user1: Context, user1: User) -> None:
    context = context_with_user1

    view = (await context.write_water(user1.id, None)).unwrap()

    new_day_log = NewDayStateLog(day=view.day)
    new_record_log = NewRecordLog(record=view.new_record)

    assert context.logger.registred_user_logs == tuple()
    assert context.logger.registered_user_registration_logs == tuple()
    assert context.logger.record_without_day_logs == tuple()
    assert context.logger.new_day_logs == tuple()
    assert context.logger.new_day_state_logs == (new_day_log, )
    assert context.logger.new_record_logs == (new_record_log, )
    assert context.logger.record_cancellation_logs == tuple()

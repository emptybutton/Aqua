from datetime import UTC, datetime
from uuid import uuid4

from pytest import fixture

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Created, Entities, FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import (
    User,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    WaterBalance,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


@fixture
def user() -> User:
    target = Target(
        water_balance=WaterBalance(water=Water.with_(milliliters=2000).unwrap())
    )

    return User(
        id=uuid4(),
        events=list(),
        weight=None,
        target=target,
        glass=Glass(capacity=Water.with_(milliliters=400).unwrap()),
        days=Entities(),
        records=Entities(),
    )


@fixture
def current_time() -> Time:
    return Time.with_(datetime_=datetime.now(UTC)).unwrap()


def test_day(user: User, current_time: Time) -> None:
    effect = SearchableEffect()
    output = user.write_water(current_time=current_time, effect=effect)

    assert output.day.user_id == user.id
    assert output.day.target == user.target
    assert output.day.water_balance == WaterBalance(
        water=Water.with_(milliliters=400).unwrap()
    )


def test_day_with_water(user: User, current_time: Time) -> None:
    effect = SearchableEffect()
    water = Water.with_(milliliters=1000).unwrap()
    output = user.write_water(water, current_time=current_time, effect=effect)

    assert output.day.user_id == user.id
    assert output.day.target == user.target
    assert output.day.water_balance == WaterBalance(
        water=Water.with_(milliliters=1000).unwrap()
    )


def test_new_record_with_water(user: User, current_time: Time) -> None:
    effect = SearchableEffect()
    water = Water.with_(milliliters=1000).unwrap()
    output = user.write_water(water, current_time=current_time, effect=effect)

    assert output.new_record.user_id == user.id
    assert output.new_record.drunk_water == water
    assert output.new_record.recording_time == current_time
    assert output.new_record.events == [Created(entity=output.new_record)]


def test_previous_records_with_multiple_call(
    user: User, current_time: Time
) -> None:
    effect = SearchableEffect()
    a = user.write_water(current_time=current_time, effect=effect)
    b = user.write_water(current_time=current_time, effect=effect)
    c = user.write_water(current_time=current_time, effect=effect)
    d = user.write_water(current_time=current_time, effect=effect)

    assert not a.previous_records
    assert b.previous_records == FrozenEntities([a.new_record])
    assert c.previous_records == FrozenEntities([a.new_record, b.new_record])
    assert d.previous_records == FrozenEntities([
        a.new_record,
        b.new_record,
        c.new_record,
    ])


def test_effect_days_with_multiple_call(user: User, current_time: Time) -> None:
    effect = SearchableEffect()
    a = user.write_water(current_time=current_time, effect=effect)
    b = user.write_water(current_time=current_time, effect=effect)
    c = user.write_water(current_time=current_time, effect=effect)
    d = user.write_water(current_time=current_time, effect=effect)

    days = effect.entities_that(Day)

    excepted_days = FrozenEntities([a.day, b.day, c.day, d.day])
    assert len(excepted_days) == 1
    assert days == excepted_days


def test_effect_records_with_multiple_call(
    user: User, current_time: Time
) -> None:
    effect = SearchableEffect()
    a = user.write_water(current_time=current_time, effect=effect)
    b = user.write_water(current_time=current_time, effect=effect)
    c = user.write_water(current_time=current_time, effect=effect)
    d = user.write_water(current_time=current_time, effect=effect)

    records = effect.entities_that(Record)

    excepted_days = FrozenEntities([
        a.new_record,
        b.new_record,
        c.new_record,
        d.new_record,
    ])
    assert len(excepted_days) == 4
    assert records == excepted_days

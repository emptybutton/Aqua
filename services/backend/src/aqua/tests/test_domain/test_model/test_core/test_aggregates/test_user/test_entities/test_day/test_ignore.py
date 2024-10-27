from datetime import UTC, datetime
from uuid import UUID

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
    NewWaterBalance,
)
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


def test_day() -> None:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()
    day = Day(
        id=UUID(int=4),
        user_id=UUID(int=0),
        events=list(),
        date_=current_time.datetime_.date(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=800).unwrap()),
        pinned_result=None,
    )
    record = Record(
        id=UUID(int=5),
        user_id=UUID(int=0),
        events=list(),
        drunk_water=Water.with_(milliliters=500).unwrap(),
        recording_time=current_time,
        is_cancelled=False,
    )
    new_water_balance = WaterBalance(
        water=Water.with_(milliliters=300).unwrap()
    )
    event = NewWaterBalance(entity=day, new_water_balance=new_water_balance)

    day.ignore(record, effect=SearchableEffect())

    assert day.water_balance == new_water_balance
    assert day.events == [event]


def test_effect() -> None:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()
    day = Day(
        id=UUID(int=4),
        user_id=UUID(int=0),
        events=list(),
        date_=current_time.datetime_.date(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        water_balance=WaterBalance(water=Water.with_(milliliters=800).unwrap()),
        pinned_result=None,
    )
    record = Record(
        id=UUID(int=5),
        user_id=UUID(int=0),
        events=list(),
        drunk_water=Water.with_(milliliters=300).unwrap(),
        recording_time=current_time,
        is_cancelled=False,
    )
    effect = SearchableEffect()

    day.ignore(record, effect=effect)

    assert effect.entities_that(Day) == FrozenEntities([day])
    assert not effect.entities_that(Record)

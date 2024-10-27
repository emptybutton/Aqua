from datetime import UTC, datetime
from uuid import UUID

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.framework.entity import Created, FrozenEntities
from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water


def test_result() -> None:
    user_id = UUID(int=4)
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()
    target = Target(
        water_balance=WaterBalance(water=Water.with_(milliliters=2000).unwrap())
    )

    day = Day.create(
        user_id=user_id,
        current_time=current_time,
        target=target,
        effect=SearchableEffect(),
    )

    assert day.user_id == user_id
    assert day.target == target
    assert day.date_ == current_time.datetime_.date()
    assert day.pinned_result is None
    assert day.water_balance == WaterBalance(
        water=Water.with_(milliliters=0).unwrap()
    )
    assert day.events == [Created(entity=day)]


def test_effect() -> None:
    effect = SearchableEffect()

    day = Day.create(
        user_id=UUID(int=4),
        current_time=Time.with_(datetime_=datetime.now(UTC)).unwrap(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        effect=effect,
    )

    assert effect.entities_that(Day) == FrozenEntities([day])

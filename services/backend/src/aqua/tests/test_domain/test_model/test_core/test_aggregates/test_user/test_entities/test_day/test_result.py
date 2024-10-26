from datetime import datetime
from uuid import uuid4

from aqua.domain.model.core.aggregates.user.internal.entities.day import (
    Day,
)
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.water import Water


def test_with_pined_result() -> None:
    target_water = Water.with_(milliliters=100_000).unwrap()
    day = Day(
        id=uuid4(),
        user_id=uuid4(),
        events=list(),
        date_=datetime.now().date(),
        target=Target(water_balance=WaterBalance(water=target_water)),
        water_balance=WaterBalance(water=Water.with_(milliliters=0).unwrap()),
        pinned_result=Result.good,
    )

    assert day.result is Result.good


def test_without_pined_result() -> None:
    target_water = Water.with_(milliliters=100_000).unwrap()
    day = Day(
        id=uuid4(),
        user_id=uuid4(),
        events=list(),
        date_=datetime.now().date(),
        target=Target(water_balance=WaterBalance(water=target_water)),
        water_balance=WaterBalance(water=Water.with_(milliliters=0).unwrap()),
        pinned_result=None,
    )

    assert day.result is Result.not_enough_water

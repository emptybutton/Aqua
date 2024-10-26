from uuid import uuid4

from result import Err, Ok

from aqua.domain.model.core.aggregates.user.root import (
    NoWeightForSuitableWaterBalanceError,
    User,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    ExtremeWeightForSuitableWaterBalanceError,
    WaterBalance,
)
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


def test_valid() -> None:
    user = User(
        id=uuid4(),
        events=list(),
        weight=Weight.with_(kilograms=70).unwrap(),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        days=set(),
        records=set(),
    )

    result = user.suitable_water_balance

    water = Water.with_(milliliters=2000).unwrap()
    assert result == Ok(WaterBalance(water=water))


def test_without_weight() -> None:
    user = User(
        id=uuid4(),
        events=list(),
        weight=None,
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        days=set(),
        records=set(),
    )

    result = user.suitable_water_balance

    assert result == Err(NoWeightForSuitableWaterBalanceError())


def test_with_extreme_weight() -> None:
    user = User(
        id=uuid4(),
        events=list(),
        weight=Weight.with_(kilograms=2000).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=Target(
            water_balance=WaterBalance(
                water=Water.with_(milliliters=2000).unwrap()
            )
        ),
        days=set(),
        records=set(),
    )

    result = user.suitable_water_balance

    assert result == Err(ExtremeWeightForSuitableWaterBalanceError())

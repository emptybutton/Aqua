from uuid import UUID

from result import Err

from aqua.domain.framework.effects.searchable import SearchableEffect
from aqua.domain.model.access.entities.user import User as AccessUser
from aqua.domain.model.core.aggregates.user.root import (
    NoWeightForSuitableWaterBalanceError,
    TranslatedFromAccess,
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


def test_without_weight_and_target() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    user_result = User.translated_from(
        access_user,
        weight=None,
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=None,
        effect=SearchableEffect(),
    )

    assert user_result == Err(NoWeightForSuitableWaterBalanceError())


def test_without_target_and_with_extreme_weight() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    user_result = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=20_000).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=None,
        effect=SearchableEffect(),
    )

    assert user_result == Err(ExtremeWeightForSuitableWaterBalanceError())


def test_target_without_weight() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    target = Target(water_balance=WaterBalance(
        water=Water.with_(milliliters=2000).unwrap()
    ))
    user = User.translated_from(
        access_user,
        weight=None,
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=target,
        effect=SearchableEffect(),
    ).unwrap()

    assert user.target == target


def test_target() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    target = Target(water_balance=WaterBalance(
        water=Water.with_(milliliters=2000).unwrap()
    ))
    user = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=100).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=target,
        effect=SearchableEffect(),
    ).unwrap()

    assert user.target == target


def test_target_without_target() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    user = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=70).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=None,
        effect=SearchableEffect(),
    ).unwrap()

    target = Target(water_balance=user.suitable_water_balance.unwrap())
    assert user.target == target


def test_glass_without_glass() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    user = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=70).unwrap(),
        glass=None,
        target=None,
        effect=SearchableEffect(),
    ).unwrap()

    assert user.glass == Glass(capacity=Water.with_(milliliters=200).unwrap())


def test_events() -> None:
    access_user = AccessUser(id=UUID(int=4), events=list())
    target = Target(water_balance=WaterBalance(
        water=Water.with_(milliliters=2000).unwrap()
    ))
    user = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=100).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=target,
        effect=SearchableEffect(),
    ).unwrap()

    assert user.events == [TranslatedFromAccess(entity=user, from_=access_user)]


def test_effect() -> None:
    effect = SearchableEffect()
    access_user = AccessUser(id=UUID(int=4), events=list())
    target = Target(water_balance=WaterBalance(
        water=Water.with_(milliliters=2000).unwrap()
    ))
    user = User.translated_from(
        access_user,
        weight=Weight.with_(kilograms=100).unwrap(),
        glass=Glass(capacity=Water.with_(milliliters=200).unwrap()),
        target=target,
        effect=effect,
    ).unwrap()

    assert set(effect.entities_that(User)) == {user}
    assert set(effect.entities_that(AccessUser)) == set()

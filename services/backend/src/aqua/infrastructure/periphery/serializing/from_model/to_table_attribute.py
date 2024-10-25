from datetime import datetime

from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


class InvalidResultValueError(Exception): ...


def result_of(result_value: int) -> Result:
    match result_value:
        case 1:
            return Result.good
        case 2:
            return Result.not_enough_water
        case 3:
            return Result.excess_water
        case _:
            raise InvalidResultValueError


class UnhandledResultError(Exception): ...


def result_value_of(result: Result) -> int:
    match result:
        case Result.good:
            return 1
        case Result.not_enough_water:
            return 2
        case Result.excess_water:
            return 3
        case _:
            raise UnhandledResultError


def maybe_result_of(result_value: int | None) -> Result | None:
    match result_value:
        case None:
            return None
        case _:
            return result_value_of(result_value)


def maybe_result_value_of(result: Result | None) -> int | None:
    match result:
        case None:
            return None
        case _:
            return result_value_of(result)


def water_of(milliliters: int) -> Water:
    return Water.with_(milliliters=milliliters).unwrap()


def water_value_of(water: Water) -> int:
    return water.milliliters


def weight_of(killograms: int | None) -> Weight | None:
    if killograms is None:
        return None

    return Weight.with_(killograms=killograms).unwrap()


def weight_value_of(weight: Weight | None) -> int | None:
    if weight is None:
        return None

    return weight.killograms


def glass_of(milliliters: int) -> Glass:
    return Glass(capacity=water_of(milliliters))


def glass_value_of(glass: Glass) -> Glass:
    return glass.capacity.milliliters


def water_balance_of(milliliters: int) -> WaterBalance:
    return WaterBalance(water=water_of(milliliters))


def water_balance_value_of(water_balance: WaterBalance) -> WaterBalance:
    return water_balance.water.milliliters


def target_of(milliliters: int) -> Target:
    return Target(water_balance=WaterBalance(water=water_of(milliliters)))


def target_value_of(target: Target) -> int:
    return target.water_balance.water.milliliters


def maybe_target_of(milliliters: int | None) -> Target | None:
    if milliliters is None:
        return None

    return Target(water_balance=WaterBalance(water=water_of(milliliters)))


def maybe_target_value_of(target: Target | None) -> int | None:
    if target is None:
        return None

    return target.water_balance.water.milliliters


def time_of(datetime_: datetime) -> Time:
    return Time(datetime_=datetime_).unwrap()


def time_value_of(time: Time) -> datetime:
    return time.datetime_

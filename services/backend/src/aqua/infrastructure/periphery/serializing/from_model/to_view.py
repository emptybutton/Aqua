from datetime import datetime

from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


class UnhandledResultError(Exception): ...


def new_result_view_of(result: Result) -> str:
    match result:
        case Result.good:
            return "good"
        case Result.not_enough_water:
            return "not_enough_water"
        case Result.excess_water:
            return "excess_water"
        case _:
            raise UnhandledResultError


def old_result_view_of(result: Result) -> int:
    match result:
        case Result.good:
            return 1
        case Result.not_enough_water:
            return 2
        case Result.excess_water:
            return 3
        case _:
            raise UnhandledResultError


def glass_view_of(glass: Glass) -> int:
    return glass.capacity.milliliters


def water_balance_view_of(water_balance: WaterBalance) -> int:
    return water_balance.water.milliliters


def target_view_of(target: Target) -> int:
    return target.water_balance.water.milliliters


def time_view_of(time: Time) -> datetime:
    return time.datetime_


def water_view_of(water: Water) -> int:
    return water.milliliters


def maybe_weight_view_of(weight: Weight | None) -> int | None:
    if weight is None:
        return None

    return weight.kilograms

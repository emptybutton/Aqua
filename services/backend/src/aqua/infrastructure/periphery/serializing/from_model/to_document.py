from datetime import datetime

from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


class UnhandledResultError(Exception): ...


def document_result_of(result: Result) -> int:
    match result:
        case Result.good:
            return 1
        case Result.not_enough_water:
            return 2
        case Result.excess_water:
            return 3
        case _:
            raise UnhandledResultError


def maybe_document_result_of(result: Result | None) -> int | None:
    if result is None:
        return None

    return document_result_of(result)


def document_water_of(water: Water) -> int:
    return water.milliliters


def maybe_document_weight_of(weight: Weight | None) -> int | None:
    if weight is None:
        return None

    return weight.kilograms


def document_glass_of(glass: Glass) -> int:
    return glass.capacity.milliliters


def document_water_balance_of(water_balance: WaterBalance) -> int:
    return water_balance.water.milliliters


def document_target_of(target: Target) -> int:
    return target.water_balance.water.milliliters


def maybe_document_target_of(target: Target | None) -> int | None:
    if target is None:
        return None

    return target.water_balance.water.milliliters


def document_time_of(time: Time) -> datetime:
    return time.datetime_

from datetime import datetime

from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Result, Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from aqua.infrastructure.periphery.serializing.from_document.to_native import (
    native_datetime_of,
)


class InvalidResultValueError(Exception): ...


def result_of(document_result: int) -> Result:
    match document_result:
        case 1:
            return Result.good
        case 2:
            return Result.not_enough_water
        case 3:
            return Result.excess_water
        case _:
            raise InvalidResultValueError


def maybe_result_of(document_result: int | None) -> Result | None:
    if document_result is None:
        return None

    return result_of(document_result)


def water_of(document_water: int) -> Water:
    return Water.with_(milliliters=document_water).unwrap()


def maybe_weight_of(maybe_document_weight: int | None) -> Weight | None:
    if maybe_document_weight is None:
        return None

    return Weight.with_(kilograms=maybe_document_weight).unwrap()


def glass_of(document_glass: int) -> Glass:
    return Glass(capacity=water_of(document_glass))


def water_balance_of(document_water_balance: int) -> WaterBalance:
    return WaterBalance(water=water_of(document_water_balance))


def target_of(document_target: int) -> Target:
    return Target(water_balance=WaterBalance(water=water_of(document_target)))


def maybe_target_of(maybe_document_target: int | None) -> Target | None:
    if maybe_document_target is None:
        return None

    water = water_of(maybe_document_target)
    return Target(water_balance=WaterBalance(water=water))


def time_of(document_time: datetime) -> Time:
    return Time.with_(datetime_=native_datetime_of(document_time)).unwrap()

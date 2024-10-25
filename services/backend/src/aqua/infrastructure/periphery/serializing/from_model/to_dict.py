from typing import Any

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User
from aqua.domain.model.core.vos.target import Result


def user_dict_of(user: User, *, name: str = "user") -> dict[str, Any]:
    suitable_milliliters = user.suitable_water_balance.map(
        lambda balance: balance.water.milliliters
    ).unwrap_or(None)

    kilograms = None if user.weight is None else user.weight.kilograms

    return {
        f"{name}_id": user.id,
        f"{name}_weight_kilograms": kilograms,
        f"{name}_glass_capacity_milliliters": user.glass.capacity.milliliters,
        f"{name}_target_water_balance_milliliters": (
            user.target.water_balance.water.milliliters
        ),
        f"{name}_suitable_water_balance_milliliters": suitable_milliliters,
    }


def record_dict_of(record: Record, *, name: str = "record") -> dict[str, Any]:
    return {
        f"{name}_id": record.id,
        f"{name}_user_id": record.user_id,
        f"{name}_drunk_water_milliliters": record.drunk_water.milliliters,
        f"{name}_recording_time": record.recording_time,
        f"is_{name}_cancelled": record.is_cancelled,
    }


def day_dict_of(day: Day, *, name: str = "day") -> dict[str, Any]:
    pinned_result = (
        None if day.pinned_result is None else _serialized(day.pinned_result)
    )

    return {
        f"{name}_id": day.id,
        f"{name}_user_id": day.user_id,
        f"{name}_date": day.date_,
        f"{name}_target_water_balance_milliliters": (
            day.target.water_balance.water.milliliters
        ),
        f"{name}_water_balance_milliliters": (
            day.water_balance.water.milliliters
        ),
        f"{name}_pinned_result": pinned_result,
        f"{name}_correct_result": _serialized(day.correct_result),
        f"{name}_result": _serialized(day.result),
    }


def _serialized(result: Result) -> str:
    match result:
        case Result.good:
            return "good"
        case Result.not_enough_water:
            return "not_enough_water"
        case Result.excess_water:
            return "excess_water"

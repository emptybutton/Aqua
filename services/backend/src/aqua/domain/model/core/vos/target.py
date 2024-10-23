from dataclasses import dataclass
from enum import Enum, auto

from aqua.domain.model.core.vos.water_balance import WaterBalance


@dataclass(kw_only=True, frozen=True, slots=True)
class Target:
    water_balance: WaterBalance


class Result(Enum):
    good = auto()
    not_enough_water = auto()
    excess_water = auto()


def result_of(target: Target, *, water_balance: WaterBalance) -> Result:
    min_required_quantity = target.water_balance.water.milliliters - 150
    max_required_quantity = target.water_balance.water.milliliters + 150

    if water_balance.water.milliliters < min_required_quantity:
        return Result.not_enough_water

    if water_balance.water.milliliters > max_required_quantity:
        return Result.excess_water

    return Result.good

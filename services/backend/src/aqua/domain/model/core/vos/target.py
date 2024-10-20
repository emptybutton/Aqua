from dataclasses import dataclass
from typing import Literal

from aqua.domain.model.core.vos.water_balance import WaterBalance


@dataclass(kw_only=True, frozen=True, slots=True)
class Target:
    water_balance: WaterBalance


type Result = Literal["good", "not_enough_water", "excess_water"]


def result_of(target: Target, *, water_balance: WaterBalance) -> Result:
    min_required_quantity = target.water_balance.water.milliliters - 150
    max_required_quantity = target.water_balance.water.milliliters + 150

    if water_balance.water.milliliters < min_required_quantity:
        return "not_enough_water"

    if max_required_quantity < water_balance.water.milliliters:
        return "excess_water"

    return "good"

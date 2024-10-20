from dataclasses import dataclass
from typing import Literal

from result import Err, Ok, Result

from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


@dataclass(kw_only=True, frozen=True, slots=True)
class WaterBalance:
    water: Water

    @classmethod
    def suitable_when(cls, *, weight: Weight) -> Result[
        "WaterBalance", Literal["extreme_weight_for_suitable_water_balance"]
    ]:
        if weight.kilograms < 30 or weight.kilograms > 150:
            return Err("extreme_weight_for_suitable_water_balance")

        suitable_milliliters = 1500 + (weight.kilograms - 20) * 10
        water = Water.with_(milliliters=suitable_milliliters).unwrap()

        return Ok(WaterBalance(water=water))

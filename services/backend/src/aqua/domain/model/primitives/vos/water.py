from dataclasses import dataclass
from typing import Literal

from result import Err, Ok, Result

from shared.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class Water(SafeImmutable):
    milliliters: int

    @classmethod
    def with_(cls, *, milliliters: int) -> Result[
        "Water", Literal["negative_water_amount"]
    ]:
        if milliliters < 0:
            return Err("negative_water_amount")

        return Ok(Water(milliliters=milliliters, is_safe=True))

    def __add__(self, water: "Water") -> "Water":
        return Water(
            milliliters=self.milliliters + water.milliliters,
            is_safe=True,
        )

    def __sub__(self, water: "Water") -> Result[
        "Water", Literal["negative_water_amount"]
    ]:
        return Water.with_(milliliters=self.milliliters - water.milliliters)

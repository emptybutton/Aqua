from dataclasses import dataclass

from result import Err, Ok, Result

from aqua.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class NegativeWaterAmountError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Water(SafeImmutable):
    milliliters: int

    @classmethod
    def with_(
        cls, *, milliliters: int
    ) -> Result["Water", NegativeWaterAmountError]:
        if milliliters < 0:
            return Err(NegativeWaterAmountError())

        return Ok(Water(milliliters=milliliters, is_safe=True))

    def __add__(self, water: "Water") -> "Water":
        return Water(
            milliliters=self.milliliters + water.milliliters,
            is_safe=True,
        )

    def __sub__(
        self, water: "Water"
    ) -> Result["Water", NegativeWaterAmountError]:
        return Water.with_(milliliters=self.milliliters - water.milliliters)

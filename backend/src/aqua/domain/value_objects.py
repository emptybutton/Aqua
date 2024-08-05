from dataclasses import dataclass
from enum import Enum, auto

from aqua.domain import errors


@dataclass(frozen=True)
class Water:
    milliliters: int

    def __post_init__(self) -> None:
        if self.milliliters < 0:
            raise errors.IncorrectWaterAmount()

    def __add__(self, water: "Water") -> "Water":
        return Water(self.milliliters + water.milliliters)


@dataclass(frozen=True)
class WaterBalance:
    water: Water


@dataclass(frozen=True)
class Glass:
    capacity: Water


@dataclass(frozen=True)
class Weight:
    kilograms: int

    def __post_init__(self) -> None:
        if self.kilograms < 0:
            raise errors.IncorrectWeightAmount()


class WaterBalanceStatus(Enum):
    good = auto()
    not_enough_water = auto()
    excess_water = auto()


def status_of(
    water_balance: WaterBalance,
    *,
    target: WaterBalance,
) -> WaterBalanceStatus:
    min_required_quantity = target.water.milliliters - 150
    max_required_quantity = target.water.milliliters + 150

    if water_balance.water.milliliters < min_required_quantity:
        return WaterBalanceStatus.not_enough_water

    if max_required_quantity < water_balance.water.milliliters:
        return WaterBalanceStatus.excess_water

    return WaterBalanceStatus.good

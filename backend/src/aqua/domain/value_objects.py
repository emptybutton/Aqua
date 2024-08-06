from dataclasses import dataclass
from enum import Enum, auto

from aqua.domain import errors


@dataclass(kw_only=True, frozen=True)
class Water:
    milliliters: int

    def __post_init__(self) -> None:
        if self.milliliters < 0:
            raise errors.IncorrectWaterAmount()

    def __add__(self, water: "Water") -> "Water":
        return Water(milliliters=self.milliliters + water.milliliters)


@dataclass(kw_only=True, frozen=True)
class WaterBalance:
    class Status(Enum):
        good = auto()
        not_enough_water = auto()
        excess_water = auto()

    water: Water

    def status_when(self, *, target: "WaterBalance") -> Status:
        min_required_quantity = target.water.milliliters - 150
        max_required_quantity = target.water.milliliters + 150

        if self.water.milliliters < min_required_quantity:
            return WaterBalance.Status.not_enough_water

        if max_required_quantity < self.water.milliliters:
            return WaterBalance.Status.excess_water

        return WaterBalance.Status.good


@dataclass(kw_only=True, frozen=True)
class Glass:
    capacity: Water


@dataclass(kw_only=True, frozen=True)
class Weight:
    kilograms: int

    def __post_init__(self) -> None:
        if self.kilograms < 0:
            raise errors.IncorrectWeightAmount()

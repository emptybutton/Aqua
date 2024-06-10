from dataclasses import dataclass

from src.aqua.domain import errors


@dataclass(frozen=True)
class Water:
    milliliters: int

    def __post_init__(self) -> None:
        if self.milliliters <= 0:
            raise errors.IncorrectWaterAmount()


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
        if self.kilograms <= 0:
            raise errors.IncorrectWeightAmount()

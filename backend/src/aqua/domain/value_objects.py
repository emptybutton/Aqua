from dataclasses import dataclass

from src.aqua.domain import errors


@dataclass(frozen=True)
class Water:
    milligrams: int

    def __post_init__(self) -> None:
        if self.milligrams <= 0:
            raise errors.IncorrectWaterAmount()


@dataclass(frozen=True)
class Weight:
    kilograms: int

    def __post_init__(self) -> None:
        if self.kilograms <= 0:
            raise errors.IncorrectWeightAmount()

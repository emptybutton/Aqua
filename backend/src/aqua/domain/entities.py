from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional
from uuid import uuid4

from src.aqua.domain.value_objects import Water, Weight
from src.aqua.domain import errors


@dataclass
class Record:
    drunk_water: Water
    user_id: int
    recording_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    id: int = field(default_factory=lambda: uuid4().int)


@dataclass
class User:
    weight: Optional[Weight]
    glass: Optional[Water]
    __water_balance: Optional[Water] = field(default=None)
    id: int = field(default_factory=lambda: uuid4().int)

    @property
    def water_balance(self) -> Water:
        assert self.__water_balance is not None
        return self.__water_balance

    def __post_init__(self) -> None:
        if self.__water_balance is None:
            self.__water_balance = self.calculate_water_balance()

    def calculate_water_balance(self) -> Water:
        if self.weight is None:
            raise errors.NoWeightForWaterBalance()

        if self.weight.kilograms <= 30 or self.weight.kilograms >= 150:  # noqa: PLR2004
            raise errors.ExtremeWeightForWaterBalance()

        return Water(1500 + (self.weight.kilograms - 20) * 10)

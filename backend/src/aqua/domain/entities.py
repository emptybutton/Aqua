from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.aqua.domain.ports import repos
from src.aqua.domain.value_objects import Water, Weight
from src.aqua.domain import errors


@dataclass
class Record:
    drunk_water: Water
    recording_time: datetime = field(default_factory=datetime.now)
    id: Optional[int] = None


@dataclass
class User:
    records: repos.Values[Record]
    water_balance: Optional[Water]
    glass: Optional[Water]
    weight: Optional[Weight]
    id: Optional[int] = None

    def __post_init__(self) -> None:
        if self.water_balance is None:
            self.water_balance = self.calculate_water_balance()

    def calculate_water_balance(self) -> Water:
        if self.weight is None:
            raise errors.NoWeightForWaterBalance()

        if self.weight.kilograms <= 30 or self.weight.kilograms >= 150:  # noqa: PLR2004
            raise errors.ExtremeWeightForWaterBalance()

        return Water(1500 + (self.weight.kilograms - 20) * 10)

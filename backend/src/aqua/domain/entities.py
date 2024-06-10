from dataclasses import dataclass, field
from datetime import datetime, UTC
from typing import Optional
from uuid import uuid4

from src.aqua.domain.value_objects import Water, WaterBalance, Glass, Weight
from src.aqua.domain import errors


@dataclass
class Record:
    drunk_water: Water
    user_id: int
    __recording_time: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    id: int = field(default_factory=lambda: uuid4().int)

    @property
    def recording_time(self) -> datetime:
        return self.__recording_time

    @recording_time.setter
    def recording_time(self, recording_time: datetime) -> None:
        if recording_time.tzinfo is not UTC:
            raise errors.NotUTCRecordingTime()

        self.__recording_time = recording_time

    def __post_init__(self) -> None:
        self.recording_time = self.__recording_time


@dataclass
class User:
    weight: Optional[Weight]
    glass: Optional[Glass]
    __water_balance: Optional[WaterBalance] = field(default=None)
    id: int = field(default_factory=lambda: uuid4().int)

    @property
    def water_balance(self) -> WaterBalance:
        assert self.__water_balance is not None
        return self.__water_balance

    def __post_init__(self) -> None:
        if self.__water_balance is None:
            self.__water_balance = self.calculate_water_balance()

    def calculate_water_balance(self) -> WaterBalance:
        if self.weight is None:
            raise errors.NoWeightForWaterBalance()

        if self.weight.kilograms <= 30 or self.weight.kilograms >= 150:  # noqa: PLR2004
            raise errors.ExtremeWeightForWaterBalance()

        return WaterBalance(Water(1500 + (self.weight.kilograms - 20) * 10))

    def write_water(self, water: Optional[Water]) -> Record:
        if water is None:
            if self.glass is None:
                raise errors.NoWaterAndGlassForNewRecord()

            water = self.glass.capacity

        return Record(water, self.id)

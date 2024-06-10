from dataclasses import dataclass, field
from datetime import datetime, UTC, date
from typing import Optional
from uuid import uuid4

from src.aqua.domain.value_objects import (
    Water, WaterBalance, Glass, Weight, WaterBalanceStatus, status_of
)
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
    __target_water_balance: Optional[WaterBalance] = field(default=None)
    id: int = field(default_factory=lambda: uuid4().int)

    @property
    def target_water_balance(self) -> WaterBalance:
        assert self.__target_water_balance is not None
        return self.__target_water_balance

    def __post_init__(self) -> None:
        if self.__target_water_balance is None:
            self.__target_water_balance = self.calculate_water_balance()

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


@dataclass
class Day:
    date_: date
    user_id: int
    target_water_balance: WaterBalance
    __real_water_balance: WaterBalance
    id: int = field(default_factory=lambda: uuid4().int)
    __result: Optional[WaterBalanceStatus] = None

    @property
    def result(self) -> WaterBalanceStatus:
        return self.__result  # type: ignore[return-value]

    @property
    def real_water_balance(self) -> WaterBalance:
        return self.__real_water_balance

    @real_water_balance.setter
    def real_water_balance(self, real_water_balance: WaterBalance) -> None:
        if self.__real_water_balance == real_water_balance:
            return

        self.__real_water_balance = real_water_balance
        self.__result = status_of(
            self.real_water_balance,
            target=self.target_water_balance,
        )

    def __post_init__(self) -> None:
        if self.__result is None:
            self.__result = status_of(
                self.real_water_balance,
                target=self.target_water_balance,
            )

from dataclasses import dataclass, field
from datetime import datetime, UTC, date
from functools import reduce
from typing import Optional
from uuid import UUID, uuid4
from operator import add

from aqua.domain.value_objects import (
    Water, WaterBalance, Glass, Weight, WaterBalanceStatus, status_of
)
from aqua.domain import errors


@dataclass
class Record:
    drunk_water: Water
    user_id: UUID
    _recording_time: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )
    id: UUID = field(default_factory=uuid4)

    @property
    def recording_time(self) -> datetime:
        return self._recording_time

    @recording_time.setter
    def recording_time(self, recording_time: datetime) -> None:
        if recording_time.tzinfo is not UTC:
            raise errors.NotUTCRecordingTime()

        self._recording_time = recording_time

    def __post_init__(self) -> None:
        self.recording_time = self._recording_time


def water_balance_from(*records: Record) -> WaterBalance:
    if len(records) == 0:
        return WaterBalance(Water(0))
    if len(records) == 1:
        return WaterBalance(records[0].drunk_water)

    return WaterBalance(reduce(add, (record.drunk_water for record in records)))


@dataclass
class User:
    glass: Glass
    weight: Optional[Weight] = None
    _target_water_balance: Optional[WaterBalance] = field(default=None)
    id: UUID = field(default_factory=uuid4)

    @property
    def target_water_balance(self) -> WaterBalance:
        assert self._target_water_balance is not None
        return self._target_water_balance

    def __post_init__(self) -> None:
        if self._target_water_balance is None:
            self._target_water_balance = self.calculate_water_balance()

    def calculate_water_balance(self) -> WaterBalance:
        if self.weight is None:
            raise errors.NoWeightForWaterBalance()

        if self.weight.kilograms <= 30 or self.weight.kilograms >= 150:  # noqa: PLR2004
            raise errors.ExtremeWeightForWaterBalance()

        return WaterBalance(Water(1500 + (self.weight.kilograms - 20) * 10))

    def write_water(self, water: Optional[Water]) -> Record:
        if water is None:
            water = self.glass.capacity

        return Record(water, self.id)


@dataclass
class Day:
    user_id: UUID
    target_water_balance: WaterBalance
    _real_water_balance: WaterBalance = field(default=WaterBalance(Water(0)))
    id: UUID = field(default_factory=uuid4)
    date_: date = field(default_factory=lambda: datetime.now(UTC).date())
    _result: Optional[WaterBalanceStatus] = None

    @property
    def result(self) -> WaterBalanceStatus:
        return self._result  # type: ignore[return-value]

    @property
    def real_water_balance(self) -> WaterBalance:
        return self._real_water_balance

    @real_water_balance.setter
    def real_water_balance(self, real_water_balance: WaterBalance) -> None:
        if self._real_water_balance == real_water_balance:
            return

        self._real_water_balance = real_water_balance
        self._result = status_of(
            self.real_water_balance,
            target=self.target_water_balance,
        )

    def __post_init__(self) -> None:
        if self._result is None:
            self._result = status_of(
                self.real_water_balance,
                target=self.target_water_balance,
            )

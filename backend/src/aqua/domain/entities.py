from dataclasses import dataclass, field, InitVar
from datetime import datetime, UTC, date
from functools import reduce
from uuid import UUID, uuid4
from operator import add

from aqua.domain.value_objects import Water, WaterBalance, Glass, Weight
from aqua.domain import errors


@dataclass(kw_only=True)
class Record:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    drunk_water: Water
    _recording_time: datetime = field(
        default_factory=lambda: datetime.now(UTC)
    )

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
        return WaterBalance(water=Water(milliliters=0))
    if len(records) == 1:
        return WaterBalance(water=records[0].drunk_water)

    sum_drunk_water = reduce(add, (record.drunk_water for record in records))
    return WaterBalance(water=sum_drunk_water)


@dataclass(kw_only=True)
class User:
    id: UUID = field(default_factory=uuid4)
    weight: Weight | None = None
    glass: Glass
    _target: WaterBalance | None = None

    @property
    def target(self) -> WaterBalance:
        return self._target  # type: ignore[return-value]

    @target.setter
    def target(self, target: WaterBalance) -> None:
        self._target = target

    @property
    def appropriate_water_balance(self) -> WaterBalance:
        if self.weight is None:
            raise errors.NoWeightForWaterBalance()

        if self.weight.kilograms <= 30 or self.weight.kilograms >= 150:  # noqa: PLR2004
            raise errors.ExtremeWeightForWaterBalance()

        appropriate_milliliters = 1500 + (self.weight.kilograms - 20) * 10
        return WaterBalance(water=Water(milliliters=appropriate_milliliters))

    def __post_init__(self) -> None:
        if self.target is None:
            self.target = self.appropriate_water_balance

    def write_water(self, water: Water | None = None) -> Record:
        if water is None:
            water = self.glass.capacity

        return Record(drunk_water=water, user_id=self.id)


@dataclass(kw_only=True)
class Day:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    date_: date = field(default_factory=lambda: datetime.now(UTC).date())
    target: WaterBalance
    _water_balance: WaterBalance = WaterBalance(water=Water(milliliters=0))
    _result: WaterBalance.Status | None = None
    _is_result_pinned: bool | None = None

    @property
    def correct_result(self) -> WaterBalance.Status:
        return self.water_balance.status_when(target=self.target)

    @property
    def result(self) -> WaterBalance.Status:
        return self._result  # type: ignore[return-value]

    @result.setter
    def result(self, result: WaterBalance.Status) -> None:
        self._is_result_pinned = True
        self._result = result

    @property
    def is_result_pinned(self) -> bool:
        return self._is_result_pinned  # type: ignore[return-value]

    @is_result_pinned.setter
    def is_result_pinned(self, is_result_pinned: bool) -> None:
        self._is_result_pinned = is_result_pinned

        if not self._is_result_pinned:
            self._result = self.correct_result

    @property
    def water_balance(self) -> WaterBalance:
        return self._water_balance

    @water_balance.setter
    def water_balance(self, water_balance: WaterBalance) -> None:
        if self._water_balance == water_balance:
            return

        self._water_balance = water_balance

        if not self._is_result_pinned:
            self._result = self.correct_result

    def __post_init__(self) -> None:
        if self._is_result_pinned is None:
            self._is_result_pinned = self._result is not None

        if self._result is None:
            self._result = self.correct_result

    def add(self, record: Record) -> None:
        assert self.user_id == record.user_id
        assert self.date_ == record.recording_time.date()

        water = self.water_balance.water + record.drunk_water
        self.water_balance = WaterBalance(water=water)

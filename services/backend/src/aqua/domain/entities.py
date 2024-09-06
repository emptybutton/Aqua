from dataclasses import dataclass, field
from datetime import UTC, date, datetime
from functools import reduce
from operator import add
from uuid import UUID, uuid4

from aqua.domain.value_objects import Glass, Water, WaterBalance, Weight


@dataclass(kw_only=True)
class Record:
    class Error(Exception): ...

    class NotUTCRecordingTimeError(Error): ...

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    drunk_water: Water
    _recording_time: datetime = field(default_factory=lambda: datetime.now(UTC))
    is_accidental: bool = False

    @property
    def recording_time(self) -> datetime:
        return self._recording_time

    @recording_time.setter
    def recording_time(self, recording_time: datetime) -> None:
        if recording_time.tzinfo is not UTC:
            raise Record.NotUTCRecordingTimeError

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
    class Error(Exception): ...

    class NoWeightForSuitableWaterBalanceError(Error): ...

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
    def suitable_water_balance(self) -> WaterBalance:
        if self.weight is None:
            raise User.NoWeightForSuitableWaterBalanceError

        return WaterBalance.suitable_when(weight=self.weight)

    def __post_init__(self) -> None:
        if self.target is None:
            self.target = self.suitable_water_balance

    class WritingError(Error): ...

    class NotUTCCurrentTimeForWritingError(WritingError): ...

    class OtherUserRecordForWritingError(WritingError): ...

    class OtherUserDayForWritingError(WritingError): ...

    class NotCurrentDayRecordForWritingError(WritingError): ...

    class NotCurerntDayForWritingError(WritingError): ...

    def write_water(
        self,
        water: Water | None = None,
        *,
        day_prevous_records: tuple[Record, ...] = tuple(),
        current_day: "Day | None" = None,
        current_time: datetime,
    ) -> tuple[Record, "Day"]:
        if current_time.tzinfo is not UTC:
            raise User.NotUTCCurrentTimeForWritingError

        for record in day_prevous_records:
            if record.recording_time.date() != current_time.date():
                raise User.NotCurrentDayRecordForWritingError
            if record.user_id != self.id:
                raise User.OtherUserRecordForWritingError

        if not water:
            water = self.glass.capacity

        new_record = Record(
            user_id=self.id, drunk_water=water, _recording_time=current_time
        )

        if not current_day:
            current_day = Day.empty_of(self, date_=current_time.date())

            for record in day_prevous_records:
                current_day.take_into_consideration(record)
        elif current_day.user_id != self.id:
            raise User.OtherUserDayForWritingError
        elif current_day.date_ != current_time.date():
            raise User.NotCurerntDayForWritingError

        current_day.take_into_consideration(new_record)

        return new_record, current_day


@dataclass(kw_only=True)
class Day:
    class Error(Exception): ...

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

    class ConsiderationError(Error): ...

    class OtherUserRecordForConsiderationError(ConsiderationError): ...

    class OtherDayRecordForConsiderationError(ConsiderationError): ...

    class AccidentalRecordForConsiderationError(ConsiderationError): ...

    def take_into_consideration(self, record: Record) -> None:
        if record.is_accidental:
            raise Day.AccidentalRecordForConsiderationError

        if self.user_id != record.user_id:
            raise Day.OtherUserRecordForConsiderationError

        if self.date_ != record.recording_time.date():
            raise Day.OtherDayRecordForConsiderationError

        water = self.water_balance.water + record.drunk_water
        self.water_balance = WaterBalance(water=water)

    class IgnoringError(Error): ...

    class OtherUserRecordForIgnoringError(IgnoringError): ...

    class OtherDayRecordForIgnoringError(IgnoringError): ...

    class NotAccidentalRecordForIgnoringError(IgnoringError): ...

    def ignore(self, record: Record) -> None:
        if not record.is_accidental:
            raise Day.NotAccidentalRecordForIgnoringError

        if self.user_id != record.user_id:
            raise Day.OtherUserRecordForIgnoringError

        if self.date_ != record.recording_time.date():
            raise Day.OtherDayRecordForIgnoringError

        water = self.water_balance.water - record.drunk_water
        self.water_balance = WaterBalance(water=water)

    @classmethod
    def empty_of(cls, user: User, *, date_: date) -> "Day":
        return Day(user_id=user.id, target=user.target, date_=date_)

    def __post_init__(self) -> None:
        if self._is_result_pinned is None:
            self._is_result_pinned = self._result is not None

        if self._result is None:
            self._result = self.correct_result


class RecordCancellationError(Exception): ...


class AccidentalRecordForRecordCancellationError(RecordCancellationError): ...


def cancel_record(*, record: Record, day: Day) -> None:
    if record.is_accidental:
        raise AccidentalRecordForRecordCancellationError

    record.is_accidental = True
    day.ignore(record)

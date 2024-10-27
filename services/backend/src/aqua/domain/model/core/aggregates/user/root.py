from dataclasses import dataclass
from datetime import date
from typing import Iterable
from uuid import UUID

from result import Err, Ok, Result

from aqua.domain.framework.effects.base import Effect
from aqua.domain.framework.entity import (
    Entities,
    Entity,
    FrozenEntities,
    Translated,
)
from aqua.domain.framework.fp.env import Env, Just, env, just
from aqua.domain.model.access.entities.user import User as AccessUser
from aqua.domain.model.core.aggregates.user.internal.entities import (
    day as _day,
)
from aqua.domain.model.core.aggregates.user.internal.entities import (
    record as _record,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import (
    ExtremeWeightForSuitableWaterBalanceError,
    WaterBalance,
)
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight


class TranslatedFromAccess(Translated["User", "AccessUser"]): ...


type UserEvent = TranslatedFromAccess


@dataclass(kw_only=True, frozen=True, slots=True)
class WritingOutput:
    new_record: _record.Record
    previous_records: FrozenEntities[_record.Record]
    day: _day.Day


@dataclass(kw_only=True, frozen=True, slots=True)
class CancellationOutput:
    day: _day.Day
    cancelled_record: _record.Record


@dataclass(frozen=True, slots=True)
class RecordContext:
    record: _record.Record


@dataclass(frozen=True, slots=True)
class RecordAndDayContext:
    record: _record.Record
    day: _day.Day


@dataclass(kw_only=True, frozen=True, slots=True)
class NoWeightForSuitableWaterBalanceError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class NoRecordToCancelError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class CancelledRecordToCancelError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class NoRecordDayToCancelError: ...


@dataclass(kw_only=True)
class User(Entity[UUID, UserEvent]):
    weight: Weight | None
    glass: Glass
    target: Target
    days: Entities[_day.Day]
    records: Entities[_record.Record]

    @property
    def suitable_water_balance(
        self,
    ) -> Result[
        WaterBalance,
        (
            ExtremeWeightForSuitableWaterBalanceError
            | NoWeightForSuitableWaterBalanceError
        ),
    ]:
        if self.weight is None:
            return Err(NoWeightForSuitableWaterBalanceError())

        return WaterBalance.suitable_when(weight=self.weight)

    @classmethod
    def translated_from(
        cls,
        access_user: AccessUser,
        *,
        weight: Weight | None,
        glass: Glass | None,
        target: Target | None,
        effect: Effect,
    ) -> Result[
        "User",
        (
            ExtremeWeightForSuitableWaterBalanceError
            | NoWeightForSuitableWaterBalanceError
        ),
    ]:
        if target is None:
            if weight is None:
                return Err(NoWeightForSuitableWaterBalanceError())

            balance_result = WaterBalance.suitable_when(weight=weight)
            target_result = balance_result.map(
                lambda balance: Target(water_balance=balance)
            )
        else:
            target_result = Ok(target)

        if glass is None:
            glass = Glass(capacity=Water.with_(milliliters=200).unwrap())

        user_result = target_result.map(
            lambda target: User(
                id=access_user.id,
                weight=weight,
                glass=glass,
                target=target,
                days=Entities(),
                records=Entities(),
                events=list(),
            )
        )
        user_result.map(
            lambda user: user.events.append(
                TranslatedFromAccess(entity=user, from_=access_user)
            )
        )
        user_result.map(effect.consider)

        return user_result

    def write_water(
        self,
        water: Water | None = None,
        *,
        current_time: Time,
        effect: Effect,
    ) -> WritingOutput:
        if not water:
            water = self.glass.capacity

        current_day = self.__day_of(current_time)

        if current_day is None:
            current_day = _day.Day.create(
                user_id=self.id,
                current_time=current_time,
                target=self.target,
                effect=effect,
            )
            self.days.add(current_day)

        new_record = _record.Record.create(
            user_id=self.id,
            drunk_water=water,
            current_time=current_time,
            effect=effect,
        )
        previous_records = FrozenEntities(self.__records_on(current_day.date_))
        self.records.add(new_record)
        current_day.take_into_consideration(new_record, effect=effect)

        return WritingOutput(
            day=current_day,
            new_record=new_record,
            previous_records=previous_records,
        )

    def cancel_record(
        self, *, record_id: UUID, effect: Effect
    ) -> Result[
        CancellationOutput,
        (
            Just[NoRecordToCancelError]
            | Env[RecordContext, NoRecordDayToCancelError]
            | Env[RecordAndDayContext, _record.CancelledRecordToCancelError]
        ),
    ]:
        record = self.__record_with(record_id)

        if not record:
            return Err(just(NoRecordToCancelError()))

        day = self.__day_of(record.recording_time)

        if day is None:
            error = NoRecordDayToCancelError()
            return Err(Env(RecordContext(record), error))

        result = _record.cancel(record, effect=effect).map_err(
            env(RecordAndDayContext(record, day))
        )
        result.map(lambda _: day.ignore(record, effect=effect))

        return result.map(
            lambda _: CancellationOutput(day=day, cancelled_record=record)
        )

    def __day_of(self, time: Time) -> _day.Day | None:
        for day in self.days:
            if day.date_ == time.datetime_.date():
                return day

        return None

    def __records_on(self, date_: date) -> Iterable[_record.Record]:
        for record in self.records:
            if record.recording_time.datetime_.date() == date_:
                yield record

    def __record_with(self, record_id: UUID) -> _record.Record | None:
        for record in self.records:
            if record.id == record_id:
                return record

        return None

from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from result import Err, Ok, Result

from aqua.domain.model.access.entities.user import User as AccessUser
from aqua.domain.model.core.aggregates.user.internal.entities import (
    day as _day,
)
from aqua.domain.model.core.aggregates.user.internal.entities import (
    record as _record,
)
from aqua.domain.model.core.vos.glass import Glass
from aqua.domain.model.core.vos.target import Target
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from aqua.domain.model.primitives.vos.weight import Weight
from shared.domain.framework.entity import Entity, Translated
from shared.domain.framework.ports.effect import Effect


type UserEvent = Translated["User", "AccessUser"]


@dataclass(kw_only=True, frozen=True, slots=True)
class WritingOutput:
    record: _record.Record
    day: _day.Day


@dataclass(kw_only=True)
class User(Entity[UUID, UserEvent]):
    weight: Weight | None
    glass: Glass
    target: Target
    days: set[_day.Day]
    records: set[_record.Record]

    @property
    def suitable_water_balance(self) -> Result[
        WaterBalance,
        Literal[
            "extreme_weight_for_suitable_water_balance",
            "no_weight_for_suitable_water_balance"
        ],
    ]:
        if self.weight is None:
            return Err("no_weight_for_suitable_water_balance")

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
        Literal[
            "extreme_weight_for_suitable_water_balance",
            "no_weight_for_suitable_water_balance"
        ],
    ]:
        if target is None:
            if weight is None:
                return Err("no_weight_for_suitable_water_balance")

            balance_result = WaterBalance.suitable_when(weight=weight)
            target_result = balance_result.map(
                lambda balance: Target(water_balance=balance)
            )
        else:
            target_result = Ok(target)

        if glass is None:
            glass = Glass(capacity=Water.with_(milliliters=200).unwrap())

        user_result = target_result.map(lambda target: User(
            id=access_user.id,
            weight=weight,
            glass=glass,
            target=target,
            days=set(),
            records=set(),
            events=list(),
        ))
        user_result.map(lambda user: user.events.append(
            Translated(entity=user, from_=access_user)
        ))
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
        self.records.add(new_record)
        current_day.take_into_consideration(new_record, effect=effect)

        return WritingOutput(
            day=current_day,
            record=new_record,
        )

    def cancel_record(self, *, record_id: UUID, effect: Effect) -> Result[
        None,
        Literal[
            "no_record_to_cancel",
            "cancelled_record_to_cancel",
            "no_record_day_to_cancel",
        ],
    ]:
        record = self.__record_with(record_id)

        if not record:
            return Err("no_record_to_cancel")

        day = self.__day_of(record.recording_time)

        if day is None:
            raise Err("no_record_day_to_cancel")

        result = _record.cancel(record, effect=effect)
        return result.map(lambda _: day.ignore(record, effect=effect))

    def __day_of(self, time: Time) -> _day.Day | None:
        for day in self.days:
            if day.date_ == time.datetime_.date:
                return day

        return None

    def __record_with(self, record_id: UUID) -> _record.Record | None:
        for record in self.records:
            if record.id == record_id:
                return record

        return None

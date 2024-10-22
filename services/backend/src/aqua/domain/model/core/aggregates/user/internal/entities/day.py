from dataclasses import dataclass
from datetime import date
from uuid import UUID, uuid4

from aqua.domain.model.core.aggregates.user.internal.entities import (
    record as _record,
)
from aqua.domain.model.core.vos.target import Result, Target, result_of
from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from shared.domain.framework.effects.base import Effect
from shared.domain.framework.entity import Created, Entity, Mutated


@dataclass(kw_only=True, frozen=True, slots=True)
class NewWaterBalance(Mutated["Day"]):
    new_water_balance: WaterBalance


type DayEvent = Created["Day"] | NewWaterBalance


@dataclass(kw_only=True)
class Day(Entity[UUID, DayEvent]):
    user_id: UUID
    date_: date
    target: Target
    water_balance: WaterBalance
    pinned_result: Result | None

    @property
    def is_result_pinned(self) -> bool:
        return self.pinned_result is not None

    @property
    def correct_result(self) -> Result:
        return result_of(self.target, water_balance=self.water_balance)

    @property
    def result(self) -> Result:
        return self.pinned_result or self.correct_result

    @classmethod
    def create(
        cls,
        *,
        user_id: UUID,
        current_time: Time,
        target: Target,
        effect: Effect,
    ) -> "Day":
        water = Water.with_(milliliters=0).unwrap()

        day = Day(
            id=uuid4(),
            user_id=user_id,
            date_=current_time.datetime_.date(),
            target=target,
            water_balance=WaterBalance(water=water),
            pinned_result=None,
            events=list(),
        )
        day.events.append(Created(entity=day))
        effect.consider(day)

        return day

    def take_into_consideration(
        self,
        record: _record.Record,
        *,
        effect: Effect,
    ) -> None:
        water = self.water_balance.water + record.drunk_water
        new_water_balance = WaterBalance(water=water)

        if self.water_balance == new_water_balance:
            return

        self.water_balance = new_water_balance
        self.events.append(
            NewWaterBalance(entity=self, new_water_balance=new_water_balance)
        )
        effect.consider(self)

    def ignore(self, record: _record.Record, *, effect: Effect) -> None:
        water = (self.water_balance.water - record.drunk_water).unwrap()
        new_water_balance = WaterBalance(water=water)

        self.water_balance = new_water_balance
        self.events.append(
            NewWaterBalance(entity=self, new_water_balance=new_water_balance)
        )
        effect.consider(self)

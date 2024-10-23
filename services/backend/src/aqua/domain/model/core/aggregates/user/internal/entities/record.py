from dataclasses import dataclass
from functools import reduce
from operator import add
from uuid import UUID, uuid4

from result import Err, Ok, Result

from aqua.domain.model.core.vos.water_balance import WaterBalance
from aqua.domain.model.primitives.vos.time import Time
from aqua.domain.model.primitives.vos.water import Water
from shared.domain.framework.effects.base import Effect
from shared.domain.framework.entity import Created, Entity, Mutated


@dataclass(kw_only=True, frozen=True, slots=True)
class Cancelled(Mutated["Record"]): ...


type RecordEvent = Created["Record"] | Cancelled


@dataclass(kw_only=True)
class Record(Entity[UUID, RecordEvent]):
    user_id: UUID
    drunk_water: Water
    recording_time: Time
    is_cancelled: bool

    @classmethod
    def create(
        cls,
        *,
        user_id: UUID,
        drunk_water: Water,
        current_time: Time,
        effect: Effect,
    ) -> "Record":
        record = Record(
            id=uuid4(),
            user_id=user_id,
            drunk_water=drunk_water,
            recording_time=current_time,
            is_cancelled=False,
            events=list(),
        )
        record.events.append(Created(entity=record))
        effect.consider(record)

        return record


@dataclass(kw_only=True, frozen=True, slots=True)
class CancelledRecordToCancelError: ...


def cancel(record: Record, *, effect: Effect) -> Result[
    None, CancelledRecordToCancelError
]:
    if record.is_cancelled:
        return Err(CancelledRecordToCancelError())

    record.is_cancelled = True
    record.events.append(Cancelled(entity=record))
    effect.consider(record)

    return Ok(None)


def water_balance_from(*records: Record) -> WaterBalance:
    if len(records) == 0:
        return WaterBalance(water=Water.with_(milliliters=0).unwrap())
    if len(records) == 1:
        return WaterBalance(water=records[0].drunk_water)

    sum_drunk_water = reduce(add, (record.drunk_water for record in records))
    return WaterBalance(water=sum_drunk_water)

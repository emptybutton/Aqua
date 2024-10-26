from dataclasses import dataclass

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryWritingView:
    user: User
    day: Day
    new_record: Record
    previous_records: tuple[Record, ...]

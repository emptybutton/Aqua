from dataclasses import dataclass

from aqua.domain.model.core.aggregates.user.internal.entities.day import Day
from aqua.domain.model.core.aggregates.user.internal.entities.record import (
    Record,
)
from aqua.domain.model.core.aggregates.user.root import User


@dataclass(kw_only=True, frozen=True, slots=True)
class RegistredUserLog:
    user: User


@dataclass(kw_only=True, frozen=True, slots=True)
class RegisteredUserRegistrationLog:
    user: User


@dataclass(kw_only=True, frozen=True, slots=True)
class RecordWithoutDayLog:
    record: Record


@dataclass(kw_only=True, frozen=True, slots=True)
class NewDayLog:
    day: Day


@dataclass(kw_only=True, frozen=True, slots=True)
class NewDayStateLog:
    day: Day


@dataclass(kw_only=True, frozen=True, slots=True)
class NewRecordLog:
    record: Record


@dataclass(kw_only=True, frozen=True, slots=True)
class RecordCancellationLog:
    record: Record

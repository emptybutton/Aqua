from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.access.vos import (
    session_lifetime as _session_lifetime,
)
from auth.domain.models.access.vos import time as _time
from shared.domain.framework import entity as _entity
from shared.domain.framework.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class Extended(_entity.MutationEvent["Session"]):
    new_lifetime: _session_lifetime.SessionLifetime


@dataclass(kw_only=True, frozen=True, slots=True)
class Cancelled(_entity.MutationEvent["Session"]): ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Replaced(_entity.MutationEvent["Session"]):
    new_leader_session_id: UUID
    leader_session: "Session"


@dataclass(kw_only=True, frozen=True, slots=True)
class BecameLeader(_entity.CommentingEvent["Session"]):
    prevous_session: "Session"


SessionEvent: TypeAlias = (
    Replaced
    | BecameLeader
    | Cancelled
    | Extended
)


SessionInactivityReasons: TypeAlias = (
    Literal["replaced"]
    | Literal["expired"]
    | Literal["cancelled"]
)


@dataclass(kw_only=True, eq=False)
class Session(_entity.Entity[UUID, SessionEvent]):
    account_id: UUID
    lifetime: _session_lifetime.SessionLifetime
    is_cancelled: bool = False
    leader_session_id: UUID | None = None

    @property
    def is_replaced(self) -> bool:
        return self.leader_session_id is not None

    def is_expired_when(self, *, current_time: _time.Time) -> bool:
        return self.lifetime.is_expired_when(current_time=current_time)

    def inactivity_reasons_when(
        self, *, current_time: _time.Time
    ) -> frozenset[SessionInactivityReasons]:
        reasons: set[SessionInactivityReasons] = set()

        if self.is_replaced:
            reasons.add("replaced")

        if self.is_expired_when(current_time=current_time):
            reasons.add("expired")

        if self.is_cancelled:
            reasons.add("cancelled")

        return frozenset(reasons)

    def is_active(self, *, current_time: _time.Time) -> bool:
        return not self.inactivity_reasons_when(current_time=current_time)


def issue_session(
    *,
    account_id: UUID,
    current_time: _time.Time,
    current_session: Session | None = None,
    effect: Effect,
) -> Session:
    if current_session is not None and not current_session.is_active(
        current_time=current_time
    ):
        current_session = None

    if (
        current_session is not None
        and current_session.account_id == account_id
    ):
        extend(current_session, current_time=current_time, effect=effect)
        return current_session

    prevous_session = current_session

    lifetime = _session_lifetime.SessionLifetime(start_time=current_time)
    current_session = Session(
        id=uuid4(),
        account_id=account_id,
        lifetime=lifetime,
        events=[],
    )
    current_session.events.append(_entity.Created(entity=current_session))
    effect.consider(current_session)

    if prevous_session is not None:
        replace(prevous_session, with_=current_session, effect=effect)

    return current_session


def session_id_that_replaced(session: Session) -> UUID | None:
    return session.leader_session_id


def cancel(session: Session, *, effect: Effect) -> None:
    session.is_cancelled = True
    session.events.append(Cancelled(entity=session))
    effect.consider(session)


def extend(
    session: Session, *, current_time: _time.Time, effect: Effect
) -> None:
    extended_lifetime = _session_lifetime.extended(
        session.lifetime, current_time=current_time,
    )

    event = Extended(entity=session, new_lifetime=extended_lifetime)
    session.events.append(event)

    effect.consider(session)


def replace(
    current_session: Session, *, with_: Session, effect: Effect
) -> None:
    new_session = with_

    prevous_session, current_session = current_session, new_session
    prevous_session.leader_session_id = current_session.id

    current_session_event = BecameLeader(
        entity=current_session, prevous_session=prevous_session
    )
    prevous_session_event = Replaced(
        entity=prevous_session,
        new_leader_session_id=current_session.id,
        leader_session=prevous_session,
    )

    current_session.events.append(current_session_event)
    prevous_session.events.append(prevous_session_event)

    effect.consider(current_session)
    effect.consider(prevous_session)

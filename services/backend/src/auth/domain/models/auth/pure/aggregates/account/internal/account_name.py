from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.auth.pure.vos.time import Time
from shared.domain.pure.entity import (
    CommentingEvent,
    Created,
    Entity,
    MutationEvent,
)
from shared.domain.pure.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class BecameCurrent(MutationEvent[UUID]):
    new_taking_time: Time


@dataclass(kw_only=True, frozen=True, slots=True)
class BecamePrevious(CommentingEvent[UUID]): ...


AccountNameEvent: TypeAlias = BecameCurrent | BecamePrevious


class AccountNameError(Exception): ...


class EmptyAccountNameError(Exception): ...


@dataclass(kw_only=True, eq=False)
class AccountName(Entity[UUID, AccountNameEvent]):
    id: UUID
    account_id: UUID
    text: str
    taking_times: set[Time]

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise EmptyAccountNameError

    def become_current(self, *, current_time: Time, effect: Effect) -> None:
        self.taking_times.add(current_time)

        event = BecameCurrent(
            entity_id=self.id, new_taking_time=current_time
        )
        self.events.append(event)

        effect.consider(self)

    def become_previous(self, *, effect: Effect) -> None:
        self.events.append(BecamePrevious(entity_id=self.id))
        effect.consider(self)

    @classmethod
    def create(
        cls,
        *,
        text: str,
        current_time: Time,
        account_id: UUID,
        effect: Effect,
    ) -> "AccountName":
        account_name_id = uuid4()
        events = [
            Created(entity_id=account_name_id),
            BecameCurrent(new_taking_time=current_time),
        ]

        account_name = AccountName(
            id=account_name_id,
            account_id=account_id,
            text=text,
            taking_times={current_time},
            events=events,
        )
        effect.consider(account_name)

        return account_name

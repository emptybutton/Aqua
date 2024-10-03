from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.access.pure.vos.time import Time
from shared.domain.framework.pure.entity import (
    CommentingEvent,
    Created,
    Entity,
    MutationEvent,
)
from shared.domain.framework.pure.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class BecameCurrent(MutationEvent["AccountName"]):
    new_taking_time: Time


@dataclass(kw_only=True, frozen=True, slots=True)
class BecamePrevious(CommentingEvent["AccountName"]): ...


AccountNameEvent: TypeAlias = BecameCurrent | BecamePrevious


@dataclass(kw_only=True, eq=False)
class AccountName(Entity[UUID, AccountNameEvent]):
    class Error(Exception): ...

    class EmptyError(Error): ...

    account_id: UUID
    text: str
    taking_times: set[Time]

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise AccountName.EmptyError

    def become_current(self, *, current_time: Time, effect: Effect) -> None:
        self.taking_times.add(current_time)

        event = BecameCurrent(entity=self, new_taking_time=current_time)
        self.events.append(event)

        effect.consider(self)

    def become_previous(self, *, effect: Effect) -> None:
        self.events.append(BecamePrevious(entity=self))
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
        account_name = AccountName(
            id=uuid4(),
            account_id=account_id,
            text=text,
            taking_times={current_time},
            events=[],
        )

        account_name.events.expand((
            Created(entity=account_name),
            BecameCurrent(entity=account_name, new_taking_time=current_time),
        ))
        effect.consider(account_name)

        return account_name

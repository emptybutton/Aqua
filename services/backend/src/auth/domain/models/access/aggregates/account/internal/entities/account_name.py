from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.access.aggregates.account.internal.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.vos.time import Time
from shared.domain.framework.entity import (
    Created,
    Entity,
    MutationEvent,
)
from shared.domain.framework.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class BecameCurrent(MutationEvent["AccountName"]):
    new_taking_time: Time


@dataclass(kw_only=True, frozen=True, slots=True)
class BecamePrevious(MutationEvent["AccountName"]): ...


AccountNameEvent: TypeAlias = BecameCurrent | BecamePrevious


@dataclass(kw_only=True, eq=False)
class AccountName(Entity[UUID, AccountNameEvent]):
    class Error(Exception): ...

    class EmptyError(Error): ...

    account_id: UUID
    text: str
    taking_times: set[Time]
    is_current: bool

    def __post_init__(self) -> None:
        if len(self.text) == 0:
            raise AccountName.EmptyError

    def become_current(self, *, current_time: Time, effect: Effect) -> None:
        self.is_current = True
        self.taking_times.add(current_time)

        event = BecameCurrent(entity=self, new_taking_time=current_time)
        self.events.append(event)

        effect.consider(self)

    def become_previous(self, *, effect: Effect) -> None:
        self.is_current = False
        self.events.append(BecamePrevious(entity=self))
        effect.consider(self)

    class CreationError(Error): ...

    class TakenForCreationError(Error): ...

    @classmethod
    async def create(
        cls,
        *,
        text: str,
        current_time: Time,
        account_id: UUID,
        is_account_name_taken: _is_account_name_taken.IsAccountNameTaken,
        effect: Effect,
    ) -> "AccountName":
        account_name = AccountName(
            id=uuid4(),
            account_id=account_id,
            text=text,
            taking_times={current_time},
            is_current=True,
            events=[],
        )
        account_name.events.append(Created(entity=account_name))

        if await is_account_name_taken(account_name):
            raise AccountName.TakenForCreationError

        effect.consider(account_name)
        return account_name

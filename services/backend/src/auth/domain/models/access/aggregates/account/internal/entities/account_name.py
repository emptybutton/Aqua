from dataclasses import dataclass
from typing import Literal
from uuid import UUID, uuid4

from result import Err, Ok, Result

from auth.domain.framework.effects.base import Effect
from auth.domain.framework.entity import Created, Entity, Mutated
from auth.domain.framework.safe import SafeMutable
from auth.domain.models.access.aggregates.account.internal.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.vos.time import Time


@dataclass(kw_only=True, frozen=True, slots=True)
class BecameCurrent(Mutated["AccountName"]):
    new_taking_time: Time


@dataclass(kw_only=True, frozen=True, slots=True)
class BecamePrevious(Mutated["AccountName"]): ...


type AccountNameEvent = Created["AccountName"] | BecameCurrent | BecamePrevious


@dataclass(kw_only=True, eq=False)
class AccountName(Entity[UUID, AccountNameEvent], SafeMutable):
    account_id: UUID
    text: str
    taking_times: set[Time]
    is_current: bool

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

    @classmethod
    def with_(
        cls,
        *,
        id: UUID,
        account_id: UUID,
        text: str,
        taking_times: set[Time],
        is_current: bool,
        events: list[AccountNameEvent],
    ) -> Result["AccountName", Literal["account_name_text_is_empty"]]:
        if not text:
            return Err("account_name_text_is_empty")

        return Ok(
            AccountName(
                id=id,
                account_id=account_id,
                text=text,
                taking_times=taking_times,
                is_current=is_current,
                events=events,
                is_safe=True,
            )
        )

    @classmethod
    async def create(
        cls,
        *,
        text: str,
        current_time: Time,
        account_id: UUID,
        is_account_name_taken: _is_account_name_taken.IsAccountNameTaken,
        effect: Effect,
    ) -> Result[
        "AccountName",
        Literal["account_name_text_is_empty", "account_name_is_taken"],
    ]:
        result = AccountName.with_(
            id=uuid4(),
            account_id=account_id,
            text=text,
            taking_times={current_time},
            is_current=True,
            events=[],
        )
        name = result.ok()
        if name is None:
            return result

        name.events.append(Created(entity=name))

        if await is_account_name_taken(name):
            return Err("account_name_is_taken")

        effect.consider(name)
        return Ok(name)

        return result

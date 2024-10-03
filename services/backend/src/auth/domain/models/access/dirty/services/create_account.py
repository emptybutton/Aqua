from auth.domain.models.access.dirty.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.pure.aggregates.account.internal import (
    session as _session,
)
from auth.domain.models.access.pure.aggregates.account.root import Account
from auth.domain.models.access.pure.vos import password as _password
from auth.domain.models.access.pure.vos import time as _time
from shared.domain.framework.pure.ports.effect import Effect


class Error(Exception): ...


class AccountNameIsTakenError(Error): ...


async def create_account(
    *,
    name_text: str,
    password: _password.Password,
    effect: Effect,
    current_time: _time.Time,
    current_session: _session.Session | None,
    is_account_name_taken: _is_account_name_taken.IsAccountNameTaken,
) -> Account.CreationOutput:
    output = Account.create(
        name_text=name_text,
        password=password,
        effect=effect,
        current_time=current_time,
        current_session=current_session,
    )

    if await is_account_name_taken(output.account.current_name):
        raise AccountNameIsTakenError

    return output

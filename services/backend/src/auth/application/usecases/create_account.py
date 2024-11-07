from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import AsyncIterator, Literal, TypeAlias
from uuid import UUID

from result import Err, Ok, Result

from auth.application.adapters.specs import (
    IsAccountNameTextTakenBasedOnCache,
    IsAccountNameTextTakenInRepo,
)
from auth.application.output.log_effect import log_effect
from auth.application.output.map_effect import Mappers, map_effect
from auth.application.ports.gateway import GatewayFactory
from auth.application.ports.loggers import Logger
from auth.application.ports.mappers import MapperFactory
from auth.application.ports.repos import Accounts
from auth.application.ports.transactions import TransactionFactory
from auth.domain.framework.effects.searchable import SearchableEffect
from auth.domain.framework.result import swap
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.aggregates.account.internal.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.aggregates.account.ports.specs import (
    is_account_name_text_taken as _is_account_name_text_taken,
)
from auth.domain.models.access.vos.password import Password
from auth.domain.models.access.vos.time import Time


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session
_IsAccountNameTextTaken: TypeAlias = (
    _is_account_name_text_taken.IsAccountNameTextTaken
)


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    account: _Account
    session: _Session


@asynccontextmanager
async def create_account[AccountsT: Accounts](
    session_id: UUID | None,
    name_text: str,
    password_text: str,
    *,
    accounts: AccountsT,
    account_mapper_in: MapperFactory[AccountsT, _Account],
    account_name_mapper_in: MapperFactory[AccountsT, _AccountName],
    session_mapper_in: MapperFactory[AccountsT, _Session],
    transaction_for: TransactionFactory[AccountsT],
    gateway_to: GatewayFactory[AccountsT],
    logger: Logger,
) -> AsyncIterator[Result[
    Output,
    Literal[
        "account_name_text_is_empty",
        "account_name_is_taken",
        "password_too_short",
        "password_contains_only_small_letters",
        "password_contains_only_capital_letters",
        "password_contains_only_digits",
        "password_has_no_numbers",
    ],
]]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    match Password.with_(text=password_text):
        case Ok(v):
            password = v
        case Err(v) as r:
            yield r
            return

    async with transaction_for(accounts) as transaction:
        is_account_name_text_taken: _IsAccountNameTextTaken

        if session_id is None:
            current_session = None
            is_account_name_text_taken = IsAccountNameTextTakenInRepo(accounts)
        else:
            gateway_result = await gateway_to(
                accounts
            ).session_with_id_and_contains_account_name_with_text(
                session_id=session_id,
                account_name_text=name_text,
            )
            current_session = gateway_result.session
            is_account_name_text_taken = IsAccountNameTextTakenBasedOnCache.of(
                gateway_result,
                name_text=name_text,
                is_account_name_text_taken=IsAccountNameTextTakenInRepo(
                    accounts
                ),
            )

        effect = SearchableEffect()
        result = await _Account.create(
            name_text=name_text,
            password=password,
            effect=effect,
            current_time=current_time,
            current_session=current_session,
            is_account_name_taken=_is_account_name_taken.IsAccountNameTaken(
                is_account_name_text_taken
            ),
        )
        await swap(result).map_async(lambda _: transaction.rollback())

        await result.map_async(
            lambda output: logger.log_registration(
                account=output.account, session=output.current_session
            )
        )
        await result.map_async(lambda _: log_effect(effect, logger))
        await result.map_async(
            lambda _: map_effect(
                effect,
                Mappers(
                    (_Account, account_mapper_in(accounts)),
                    (_AccountName, account_name_mapper_in(accounts)),
                    (_Session, session_mapper_in(accounts)),
                ),
            )
        )

        yield result.map(
            lambda output: Output(
                account=output.account, session=output.current_session
            )
        )

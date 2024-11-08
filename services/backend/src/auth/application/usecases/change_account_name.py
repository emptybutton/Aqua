from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import UTC, datetime
from typing import AsyncIterator, Literal, TypeAlias
from uuid import UUID

from result import Err, Result

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
from auth.domain.models.access.vos.time import Time


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True)
class Output:
    account: _Account
    previous_account_name: _AccountName | None


@asynccontextmanager
async def change_account_name[AccountsT: Accounts](
    account_id: UUID,
    account_name_text: str,
    *,
    accounts: AccountsT,
    gateway_to: GatewayFactory[AccountsT],
    account_mapper_in: MapperFactory[AccountsT, _Account],
    account_name_mapper_in: MapperFactory[AccountsT, _AccountName],
    session_mapper_in: MapperFactory[AccountsT, _Session],
    transaction_for: TransactionFactory[AccountsT],
    logger: Logger,
) -> AsyncIterator[
    Result[
        Output,
        Literal[
            "no_account", "account_name_text_is_empty", "account_name_is_taken"
        ],
    ]
]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    async with transaction_for(accounts) as transaction:
        gateway = gateway_to(accounts)
        gateway_result = (
            await gateway.account_with_id_and_contains_account_name_with_text(
                account_id=account_id,
                account_name_text=account_name_text,
            )
        )
        account = gateway_result.account
        is_account_name_text_taken = IsAccountNameTextTakenBasedOnCache.of(
            gateway_result,
            name_text=account_name_text,
            is_account_name_text_taken=IsAccountNameTextTakenInRepo(accounts),
        )

        if not account:
            await transaction.rollback()
            yield Err("no_account")
            return

        effect = SearchableEffect()
        result = await account.change_name(
            new_name_text=account_name_text,
            current_time=current_time,
            effect=effect,
            is_account_name_taken=_is_account_name_taken.IsAccountNameTaken(
                is_account_name_text_taken
            ),
        )
        await swap(result).map_async(lambda _: transaction.rollback())

        async def act(output: _Account.NameChangeOutput) -> None:
            if output.previous_name is not None:
                await logger.log_renaming(
                    account=account,
                    current_account_name=account.current_name,
                    previous_account_name=output.previous_name,
                )

        await result.map_async(act)

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
                account=account,
                previous_account_name=output.previous_name,
            )
        )

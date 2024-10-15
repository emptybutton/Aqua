from dataclasses import dataclass
from datetime import UTC, datetime
from typing import TypeAlias, TypeVar
from uuid import UUID

from auth.application.adapters.specs import (
    IsAccountNameTextTakenBasedOnCache,
    IsAccountNameTextTakenInRepo,
)
from auth.application.output.log_effect import log_effect
from auth.application.ports.gateway import GatewayFactory
from auth.application.ports.loggers import Logger
from auth.application.ports.repos import Accounts
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.aggregates.account.internal.specs import (
    is_account_name_taken as _is_account_name_taken,
)
from auth.domain.models.access.vos.time import Time
from shared.application.adapters.effects import IndexedEffect
from shared.application.output.map_effect import Mappers, map_effect
from shared.application.ports.indexes import EmptyIndexFactory
from shared.application.ports.mappers import MapperFactory
from shared.application.ports.transactions import TransactionFactory


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True)
class Output:
    account: _Account
    previous_account_name: _AccountName | None


class Error(Exception): ...


class NoAccountError(Error): ...


_AccountsT = TypeVar("_AccountsT", bound=Accounts)


async def change_account_name(
    account_id: UUID,
    account_name_text: str,
    *,
    empty_index_factory: EmptyIndexFactory,
    accounts: _AccountsT,
    gateway_to: GatewayFactory[_AccountsT],
    account_mapper_in: MapperFactory[_AccountsT, _Account],
    account_name_mapper_in: MapperFactory[_AccountsT, _AccountName],
    session_mapper_in: MapperFactory[_AccountsT, _Session],
    transaction_for: TransactionFactory[_AccountsT],
    logger: Logger,
) -> Output:
    current_time = Time(datetime_=datetime.now(UTC))

    async with transaction_for(accounts):
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
            raise NoAccountError

        effect = IndexedEffect(empty_index_factory=empty_index_factory)
        result = await account.change_name(
            new_name_text=account_name_text,
            current_time=current_time,
            effect=effect,
            is_account_name_taken=_is_account_name_taken.IsAccountNameTaken(
                is_account_name_text_taken
            ),
        )

        if result.previous_name is not None:
            await logger.log_renaming(
                account=account,
                current_account_name=account.current_name,
                previous_account_name=result.previous_name,
            )

        await log_effect(effect, logger)
        await map_effect(
            effect,
            Mappers(
                (_Account, account_mapper_in(accounts)),
                (_AccountName, account_name_mapper_in(accounts)),
                (_Session, session_mapper_in(accounts)),
            ),
        )

        return Output(
            account=account,
            previous_account_name=result.previous_name,
        )

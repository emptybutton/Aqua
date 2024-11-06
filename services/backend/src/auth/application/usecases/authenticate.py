from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from result import Err, Result

from auth.application.output.log_effect import log_effect
from auth.application.output.map_effect import Mappers, map_effect
from auth.application.ports.loggers import Logger
from auth.application.ports.mappers import MapperFactory
from auth.application.ports.repos import Accounts
from auth.application.ports.transactions import TransactionFactory
from auth.domain.framework.effects.searchable import SearchableEffect
from auth.domain.framework.result import swap
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.vos.time import Time


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    account_id: UUID
    session_id: UUID


async def authenticate[AccountsT: Accounts](
    session_id: UUID,
    *,
    accounts: AccountsT,
    account_mapper_in: MapperFactory[AccountsT, _Account],
    account_name_mapper_in: MapperFactory[AccountsT, _AccountName],
    session_mapper_in: MapperFactory[AccountsT, _Session],
    transaction_for: TransactionFactory[AccountsT],
    logger: Logger,
) -> Result[
    Output,
    Literal[
        "no_account",
        "no_session_for_secondary_authentication",
        "expired_session_for_secondary_authentication",
        "cancelled_session_for_secondary_authentication",
        "replaced_session_for_secondary_authentication",
    ],
]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    async with transaction_for(accounts) as transaction:
        account = await accounts.account_with_session(session_id=session_id)

        if account is None:
            await transaction.rollback()
            return Err("no_account")

        effect = SearchableEffect()
        session_result = account.secondarily_authenticate(
            session_id=session_id, current_time=current_time, effect=effect
        )
        await swap(session_result).map_async(lambda _: transaction.rollback())

        await session_result.map_async(lambda _: log_effect(effect, logger))
        await session_result.map_async(lambda _: map_effect(
            effect,
            Mappers(
                (_Account, account_mapper_in(accounts)),
                (_AccountName, account_name_mapper_in(accounts)),
                (_Session, session_mapper_in(accounts)),
            ),
        ))

        return session_result.map(lambda session: (
            Output(account_id=account.id, session_id=session.id))
        )

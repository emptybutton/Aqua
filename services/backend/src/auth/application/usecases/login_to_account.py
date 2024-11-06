from dataclasses import dataclass
from datetime import UTC, datetime
from typing import Literal, TypeAlias
from uuid import UUID

from result import Err, Ok, Result

from auth.application.output.log_effect import log_effect
from auth.application.output.map_effect import Mappers, map_effect
from auth.application.ports.gateway import GatewayFactory
from auth.application.ports.loggers import Logger
from auth.application.ports.mappers import MapperFactory
from auth.application.ports.repos import Accounts
from auth.application.ports.transactions import TransactionFactory
from auth.domain.framework.effects.searchable import SearchableEffect
from auth.domain.models.access.aggregates import account as _account
from auth.domain.models.access.vos.password import Password
from auth.domain.models.access.vos.time import Time


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName
_Session: TypeAlias = _account.internal.entities.session.Session


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    account: _Account
    session: _Session


async def login_to_account[AccountsT: Accounts](
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
) -> Result[Output, Literal["no_account", "incorrect_password"]]:
    current_time = Time.with_(datetime_=datetime.now(UTC)).unwrap()

    match Password.with_(text=password_text):
        case Ok(value):
            password = value
        case Err(value):
            return Err("incorrect_password")

    async with transaction_for(accounts) as transaction:
        if session_id is None:
            current_session = None
            account = await accounts.account_with_name(name_text=name_text)
        else:
            gateway = gateway_to(accounts)
            gateway_result = (
                await gateway.session_with_id_and_account_with_name(
                    session_id=session_id,
                    account_name_text=name_text,
                )
            )
            current_session = gateway_result.session
            account = gateway_result.account

        if account is None:
            await transaction.rollback()
            return Err("no_account")

        effect = SearchableEffect()
        result = _account.root.login_to(
            account,
            password=password,
            current_time=current_time,
            current_session=current_session,
            effect=effect,
        )
        match result:
            case Ok(v):
                session = v
            case Err(v):
                await transaction.rollback()
                return Err("incorrect_password")

        await logger.log_login(account=account, session=session)
        await log_effect(effect, logger)
        await map_effect(
            effect,
            Mappers(
                (_Account, account_mapper_in(accounts)),
                (_AccountName, account_name_mapper_in(accounts)),
                (_Session, session_mapper_in(accounts)),
            ),
        )

        return Ok(Output(account=account, session=session))

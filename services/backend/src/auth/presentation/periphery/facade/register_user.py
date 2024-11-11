from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator, TypeAlias
from uuid import UUID

from result import Err, Ok

from auth.application import ports
from auth.application.usecases.create_account import (
    create_account as _create_account,
)
from auth.domain.models.access.aggregates import account as _account
from auth.infrastructure.adapters import (
    gateways,
    mappers,
    repos,
)
from auth.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)
from auth.presentation.di.containers import async_container


_Account: TypeAlias = _account.root.Account
_AccountName: TypeAlias = _account.internal.entities.account_name.AccountName


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user_id: UUID
    username: str
    session_id: UUID


class Error(Exception): ...


class TakenUsernameError(Error): ...


class EmptyUsernameError(Error): ...


class WeekPasswordError(Error): ...


@asynccontextmanager
async def perform(
    session_id: UUID | None,
    username: str,
    password: str,
) -> AsyncIterator[Output]:
    async with async_container() as container, _create_account(
        session_id,
        username,
        password,
        accounts=await container.get(repos.db.DBAccounts, "repos"),
        account_mapper_in=await container.get(
            mappers.db.account.DBAccountMapperFactory, "mappers"
        ),
        account_name_mapper_in=await container.get(
            mappers.db.account_name.DBAccountNameMapperFactory, "mappers"
        ),
        session_mapper_in=await container.get(
            mappers.db.session.DBSessionMapperFactory, "mappers"
        ),
        transaction_for=await container.get(
            DBConnectionTransactionFactory, "transactions"
        ),
        gateway_to=await container.get(
            gateways.db.DBGatewayFactory, "gateways"
        ),
        logger=await container.get(ports.loggers.Logger, "loggers"),
    ) as result:
        match result:
            case Ok(output):
                yield Output(
                    user_id=output.account.id,
                    username=output.account.current_name.text,
                    session_id=output.session.id,
                )
            case Err("account_name_text_is_empty"):
                raise EmptyUsernameError
            case Err("account_name_is_taken"):
                raise TakenUsernameError
            case Err(_):
                raise WeekPasswordError

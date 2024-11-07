from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import AsyncIterator
from uuid import UUID

from result import Err, Ok

from auth.application import ports
from auth.application.usecases import login_to_account as _login
from auth.infrastructure.adapters import (
    gateways,
    mappers,
    repos,
)
from auth.infrastructure.adapters.transactions import (
    DBConnectionTransactionFactory,
)
from auth.presentation.di.containers import async_container


@dataclass(kw_only=True, frozen=True, slots=True)
class Output:
    user_id: UUID
    username: str
    session_id: UUID


class Error(Exception): ...


class NoUserError(Error): ...


class IncorrectPasswordError(Error): ...


@asynccontextmanager
async def perform(
    session_id: UUID | None,
    name: str,
    password: str,
) -> AsyncIterator[Output]:
    async with async_container() as container, _login.login_to_account(
        session_id,
        name,
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
            case Err("no_account"):
                raise NoUserError
            case Err("incorrect_password"):
                raise IncorrectPasswordError
            case _:
                raise Error

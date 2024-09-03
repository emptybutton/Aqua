from dataclasses import dataclass
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.cases import rename_user
from auth.domain import value_objects as vos
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    new_username: str
    previous_username: str


NoUserError: TypeAlias = rename_user.NoUserError

NewUsernameTakenError: TypeAlias = rename_user.NewUsernameTakenError

EmptyUsernameError: TypeAlias = vos.Username.EmptyError

Error: TypeAlias = rename_user.Error | EmptyUsernameError


async def perform(
    user_id: UUID,
    new_username: str,
    *,
    session: AsyncSession,
) -> Output:
    async with async_container(context={AsyncSession: session}) as container:
        result = await rename_user.perform(
            user_id,
            new_username,
            users=await container.get(repos.DBUsers, "repos"),
            previous_usernames=await container.get(
                repos.DBPreviousUsernames, "repos"
            ),
            user_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
            previous_username_transaction_for=await container.get(
                DBTransactionFactory, "transactions"
            ),
        )

    return Output(
        user_id=result.user.id,
        new_username=result.user.name.text,
        previous_username=result.previous_username.username.text,
    )

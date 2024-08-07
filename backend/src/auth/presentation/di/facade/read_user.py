from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.cases import read_user
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container


@dataclass(kw_only=True, frozen=True)
class Output:
    username: str


async def perform(
    user_id: UUID,
    *,
    session: AsyncSession,
) -> Output | None:
    async with async_container(context={AsyncSession: session}) as container:
        user = await read_user.perform(
            user_id,
            users=await container.get(repos.DBUsers),
        )

    if user is None:
        return None

    return Output(username=user.name.text)

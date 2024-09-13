from sqlalchemy.ext.asyncio import AsyncSession

from auth.application.cases import user_exists
from auth.infrastructure.adapters import repos
from auth.presentation.di.containers import async_container


async def perform(username: str, *, session: AsyncSession) -> bool:
    async with async_container(context={AsyncSession: session}) as container:
        return await user_exists.perform(
            username,
            users=await container.get(repos.DBUsers, "repos"),
            previous_usernames=await container.get(
                repos.DBPreviousUsernames, "repos"
            ),
        )

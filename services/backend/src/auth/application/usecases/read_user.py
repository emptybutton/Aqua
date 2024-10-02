from uuid import UUID

from auth.application.ports import repos
from auth.domain import entities


async def perform(user_id: UUID, *, users: repos.Users) -> entities.User | None:
    return await users.find_with_id(user_id)

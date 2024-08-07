from uuid import UUID

from auth.domain import entities
from auth.application.ports import repos


async def perform(
    user_id: UUID,
    *,
    users: repos.Users,
) -> entities.User | None:
    return await users.find_with_id(user_id)

from uuid import UUID

from aqua.domain import entities
from aqua.application.ports import repos


async def perform(
    user_id: UUID,
    *,
    users: repos.Users,
) -> entities.User | None:
    return await users.find_with_id(user_id)

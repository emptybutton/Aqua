from typing import Optional
from uuid import UUID

from src.auth.domain import entities
from src.auth.application.ports import repos


async def read_user_data(
    user_id: UUID,
    *,
    users: repos.Users,
) -> Optional[entities.User]:
    return await users.get_by_id(user_id)


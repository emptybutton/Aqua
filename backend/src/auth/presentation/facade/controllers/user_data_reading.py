from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.cases import user_data_reading
from src.auth.infrastructure.adapters import repos


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    username: str


async def read_user_data(
    user_id: UUID,
    *,
    session: AsyncSession,
) -> Optional[OutputDTO]:
    user = await user_data_reading.read_user_data(
        user_id,
        users=repos.Users(session),
    )

    if user is None:
        return None

    return OutputDTO(username=user.name.text)

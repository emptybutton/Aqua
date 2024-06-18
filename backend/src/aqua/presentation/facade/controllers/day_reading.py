from datetime import date
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.aqua.application.cases import day_reading
from src.aqua.infrastructure.adapters import repos


OutputDTO: TypeAlias = day_reading.OutputDTO

BaseError: TypeAlias = day_reading.BaseError

NoUserError: TypeAlias = day_reading.NoUserError


async def read_day(
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession,
) -> OutputDTO:
    return await day_reading.read_day(
        user_id,
        date_,
        users=repos.Users(session),
        days=repos.Days(session),
    )

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import writing
from aqua.infrastructure.adapters import repos, uows
from shared.infrastructure.adapters import uows as shared_uows


BaseError: TypeAlias = writing.BaseError

NoUserError: TypeAlias = writing.NoUserError


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


async def write_water(
    user_id: UUID,
    milliliters: Optional[int],
    *,
    session: AsyncSession,
) -> OutputDTO:
    record = await writing.write_water(
        user_id,
        milliliters,
        users=repos.Users(session),
        records=repos.Records(session),
        days=repos.Days(session),
        record_uow_for=lambda _: shared_uows.DBUoW(session),
        day_uow_for=lambda _: uows.DirtyDayUoW(session),
    )

    return OutputDTO(
        user_id=record.user_id,
        record_id=record.id,
        drunk_water_milliliters=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )

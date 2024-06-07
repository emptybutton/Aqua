from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TypeAlias

from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.application import writing
from src.aqua.infrastructure.adapters import repos
from src.shared.infrastructure.adapters import uows


BaseError: TypeAlias = writing.BaseError

NoUserError: TypeAlias = writing.NoUserError

NoMillilitersError: TypeAlias = writing.NoMillilitersError


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: int
    record_id: int
    drunk_water_milliliters: int
    recording_time: datetime


async def write_water(
    user_id: int,
    milliliters: Optional[int],
    *,
    connection: AsyncConnection,
) -> OutputDTO:
    record = await writing.write_water(
        user_id,
        milliliters,
        users=repos.Users(connection),
        records=repos.Records(connection),
        uow_for=lambda _: uows.FakeUoW(),  # type: ignore[arg-type, return-value]
    )

    return OutputDTO(
        user_id=record.user_id,
        record_id=record.id,
        drunk_water_milliliters=record.drunk_water.milliliters,
        recording_time=record.recording_time,
    )

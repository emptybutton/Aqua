from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import user_data_reading
from aqua.infrastructure.adapters import repos


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: Optional[int]
    target_water_balance_milliliters: int


async def read_user_data(
    user_id: UUID,
    *,
    session: AsyncSession,
) -> Optional[OutputDTO]:
    user = await user_data_reading.read_user_data(
        user_id,
        users=repos.Users(session)
    )

    if user is None:
        return None

    weight_kilograms = None if user.weight is None else user.weight.kilograms
    water_balance_milliliters = user.target_water_balance.water.milliliters

    return OutputDTO(
        user_id=user.id,
        glass_milliliters=user.glass.capacity.milliliters,
        weight_kilograms=weight_kilograms,
        target_water_balance_milliliters=water_balance_milliliters,
    )

from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from src.aqua.application import registration
from src.aqua.infrastructure.adapters import repos
from src.shared.infrastructure.adapters import uows


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    id: UUID
    water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: Optional[int]


async def register_user(
    user_id: UUID,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    session: AsyncSession,
) -> OutputDTO:
    user = await registration.register_user(
        user_id,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
        users=repos.Users(session),
        uow_for=lambda _: uows.DBUoW(session),
    )

    weight_kilograms = None

    if user.weight is not None:
        weight_kilograms = user.weight.kilograms

    return OutputDTO(
        id=user.id,
        water_balance_milliliters=user.target_water_balance.water.milliliters,
        weight_kilograms=weight_kilograms,
        glass_milliliters=user.glass.capacity.milliliters,
    )

from dataclasses import dataclass
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.application import registration
from src.aqua.infrastructure.adapters import repos
from src.shared.infrastructure.adapters import uows


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    id: int
    water_balance_milliliters: int
    glass_milliliters: Optional[int]
    weight_kilograms: Optional[int]


async def register_user(
    user_id: int,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    connection: AsyncConnection,
) -> OutputDTO:
    user = await registration.register_user(
        user_id,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
        users=repos.Users(connection),
        uow_for=lambda _: uows.FakeUoW(),  # type: ignore[arg-type, return-value]
    )

    glass_milliliters = None
    weight_kilograms = None

    if user.glass is not None:
        glass_milliliters = user.glass.milliliters

    if user.weight is not None:
        weight_kilograms = user.weight.kilograms

    return OutputDTO(
        id=user.id,
        water_balance_milliliters=user.water_balance.milliliters,
        weight_kilograms=weight_kilograms,
        glass_milliliters=glass_milliliters,
    )
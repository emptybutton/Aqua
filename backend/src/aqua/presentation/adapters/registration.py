from dataclasses import dataclass
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncConnection

from src.aqua.application import registration
from src.aqua.infrastructure.adapters import repos
from src.shared.infrastructure.adapters import uows


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    id: int
    water_balance_milligrams: int
    glass_milligrams: Optional[int]
    weight_kilograms: Optional[int]


async def register_user(
    user_id: int,
    water_balance_milligrams: Optional[int],
    glass_milligrams: Optional[int],
    weight_kilograms: Optional[int],
    *,
    connection: AsyncConnection,
) -> OutputDTO:
    user = await registration.register_user(
        user_id,
        water_balance_milligrams,
        glass_milligrams,
        weight_kilograms,
        users=repos.Users(connection),
        uow_for=lambda _: uows.FakeUoW(),  # type: ignore[arg-type, return-value]
    )

    glass_milligrams = None
    weight_kilograms = None

    if user.glass is not None:
        glass_milligrams = user.glass.milligrams

    if user.weight is not None:
        weight_kilograms = user.weight.kilograms

    return OutputDTO(
        id=user.id,
        water_balance_milligrams=user.water_balance.milligrams,
        weight_kilograms=weight_kilograms,
        glass_milligrams=glass_milligrams,
    )

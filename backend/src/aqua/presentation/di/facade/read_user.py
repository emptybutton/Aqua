from dataclasses import dataclass
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import read_user
from aqua.application.ports import repos
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: int | None
    target_water_balance_milliliters: int


async def perform(
    user_id: UUID,
    *,
    session: AsyncSession,
) -> Output | None:
    async with adapter_container(context={AsyncSession: session}) as container:
        user = await read_user.perform(
            user_id,
            users=await container.get(repos.Users),
        )

    if user is None:
        return None

    weight_kilograms = None if user.weight is None else user.weight.kilograms
    water_balance_milliliters = user.target.water.milliliters

    return Output(
        user_id=user.id,
        glass_milliliters=user.glass.capacity.milliliters,
        weight_kilograms=weight_kilograms,
        target_water_balance_milliliters=water_balance_milliliters,
    )

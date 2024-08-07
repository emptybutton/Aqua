from dataclasses import dataclass
from datetime import date
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import read_day
from aqua.infrastructure import adapters
from aqua.presentation.di.containers import adapter_container


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    target_water_balance: int
    real_water_balance: int
    result_code: int


Error: TypeAlias = read_day.Error

NoUserError: TypeAlias = read_day.NoUserError


async def perform(
    user_id: UUID,
    date_: date,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await read_day.perform(
            user_id,
            date_,
            users=await container.get(adapters.repos.DBUsers),
            days=await container.get(adapters.repos.DBDays),
        )

    return Output(
        user_id=result.day.user_id,
        target_water_balance=result.day.target.water.milliliters,
        real_water_balance=result.day.water_balance.water.milliliters,
        result_code=result.day.result.value,
    )

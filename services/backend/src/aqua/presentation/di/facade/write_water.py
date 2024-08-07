from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import write_water
from aqua.domain import value_objects as vos
from aqua.presentation.di.containers import adapter_container
from aqua.infrastructure import adapters
from shared.infrastructure.adapters.transactions import DBTransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


IncorrectWaterAmountError: TypeAlias = vos.Water.IncorrectAmountError

NoUserError: TypeAlias = write_water.NoUserError

Error: TypeAlias = write_water.Error | IncorrectWaterAmountError


async def perform(
    user_id: UUID,
    milliliters: int | None,
    *,
    session: AsyncSession,
) -> Output:
    async with adapter_container(context={AsyncSession: session}) as container:
        result = await write_water.perform(
            user_id,
            milliliters,
            users=await container.get(adapters.repos.DBUsers),
            records=await container.get(adapters.repos.DBRecords),
            days=await container.get(adapters.repos.DBDays),
            record_transaction_for=await container.get(DBTransactionFactory),
            day_transaction_for=await container.get(DBTransactionFactory),
            user_transaction_for=await container.get(DBTransactionFactory),
        )

    return Output(
        user_id=result.record.user_id,
        record_id=result.record.id,
        drunk_water_milliliters=result.record.drunk_water.milliliters,
        recording_time=result.record.recording_time,
    )

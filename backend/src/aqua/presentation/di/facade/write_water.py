from dataclasses import dataclass
from datetime import datetime
from typing import TypeAlias
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from aqua.application.cases import write_water
from aqua.application.ports import repos
from aqua.domain import errors
from aqua.presentation.di.containers import adapter_container
from shared.presentation.di.providers import TransactionFactory


@dataclass(kw_only=True, frozen=True)
class Output:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


IncorrectWaterAmountError: TypeAlias = errors.IncorrectWaterAmount

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
            users=await container.get(repos.Users),
            records=await container.get(repos.Records),
            days=await container.get(repos.Days),
            record_transaction_for=await container.get(TransactionFactory),
            day_transaction_for=await container.get(TransactionFactory),
            user_transaction_for=await container.get(TransactionFactory),
        )

    return Output(
        user_id=result.record.user_id,
        record_id=result.record.id,
        drunk_water_milliliters=result.record.drunk_water.milliliters,
        recording_time=result.record.recording_time,
    )

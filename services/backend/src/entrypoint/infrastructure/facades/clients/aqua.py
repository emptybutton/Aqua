from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import date, datetime
from typing import AsyncIterator, Literal
from uuid import UUID

from aqua.presentation.periphery import facade as aqua


@dataclass(kw_only=True, frozen=True, slots=True)
class RecordData:
    record_id: UUID
    drunk_water_milliliters: int
    recording_time: datetime


@dataclass(kw_only=True, frozen=True, slots=True)
class Error:
    unexpected_error: Exception


async def close() -> None:
    await aqua.close.perform()


@dataclass(kw_only=True, frozen=True, slots=True)
class RegisterUserOutputData:
    user_id: UUID
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


@asynccontextmanager
async def register_user(
    auth_user_id: UUID,
    water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
) -> AsyncIterator[
    RegisterUserOutputData
    | Error
    | Literal["incorrect_water_amount"]
    | Literal["incorrect_weight_amount"]
    | Literal["no_weight_for_water_balance"]
    | Literal["extreme_weight_for_water_balance"]
]:
    register_user = aqua.register_user.perform(
        auth_user_id,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
    )

    try:
        async with register_user as result:
            target = result.target_water_balance_milliliters

            yield RegisterUserOutputData(
                user_id=result.user_id,
                target_water_balance_milliliters=target,
                glass_milliliters=result.glass_milliliters,
                weight_kilograms=result.weight_kilograms,
            )
    except aqua.register_user.IncorrectWaterAmountError:
        yield "incorrect_water_amount"
    except aqua.register_user.IncorrectWeightAmountError:
        yield "incorrect_weight_amount"
    except aqua.register_user.NoWeightForWaterBalanceError:
        yield "no_weight_for_water_balance"
    except aqua.register_user.ExtremeWeightForWaterBalanceError:
        yield "extreme_weight_for_water_balance"
    except Exception as error:
        yield Error(unexpected_error=error)


@dataclass(kw_only=True, frozen=True, slots=True)
class WriteWaterOutputData:
    user_id: UUID
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    date_: date
    previous_records: tuple[RecordData, ...]
    new_record: RecordData


@asynccontextmanager
async def write_water(
    user_id: UUID,
    milliliters: int | None,
) -> AsyncIterator[
    WriteWaterOutputData
    | Error
    | Literal["no_user"]
    | Literal["incorrect_water_amount"]
]:
    try:
        async with aqua.write_water.perform(user_id, milliliters) as result:
            target = result.target_water_balance_milliliters
            previous_records = tuple(
                map(_record_data_of, result.previous_records)
            )

            yield WriteWaterOutputData(
                user_id=result.user_id,
                target_water_balance_milliliters=target,
                water_balance_milliliters=result.water_balance_milliliters,
                result_code=result.result_code,
                real_result_code=result.real_result_code,
                is_result_pinned=result.is_result_pinned,
                date_=result.date_,
                previous_records=previous_records,
                new_record=_record_data_of(result.new_record),
            )
    except aqua.write_water.NoUserError:
        yield "no_user"
    except aqua.write_water.IncorrectWaterAmountError:
        yield "incorrect_water_amount"
    except Exception as error:
        yield Error(unexpected_error=error)


def _record_data_of(data: aqua.write_water.RecordData) -> RecordData:
    return RecordData(
        record_id=data.record_id,
        drunk_water_milliliters=data.drunk_water_milliliters,
        recording_time=data.recording_time,
    )


@dataclass(kw_only=True, frozen=True, slots=True)
class ReadDayOutputData:
    user_id: UUID
    date_: date
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    records: tuple[RecordData, ...]


async def read_day(
    user_id: UUID, date_: date
) -> (
    ReadDayOutputData
    | Error
    | Literal["no_user"]
):
    try:
        result = await aqua.read_day.perform(user_id, date_)
    except aqua.read_day.NoUserError:
        return "no_user"
    except Exception as error:
        return Error(unexpected_error=error)

    target = result.target_water_balance_milliliters
    records = tuple(
        RecordData(
            record_id=record.record_id,
            drunk_water_milliliters=record.drunk_water_milliliters,
            recording_time=record.recording_time,
        )
        for record in result.records
    )
    return ReadDayOutputData(
        user_id=result.user_id,
        date_=result.date_,
        target_water_balance_milliliters=target,
        water_balance_milliliters=result.water_balance_milliliters,
        result_code=result.result_code,
        real_result_code=result.real_result_code,
        is_result_pinned=result.is_result_pinned,
        records=records,
    )


@dataclass(kw_only=True, frozen=True, slots=True)
class ReadUserOutputData:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: int | None
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    records: tuple[RecordData, ...]


async def read_user(
    user_id: UUID
) -> (
    ReadUserOutputData
    | Error
    | Literal["no_user"]
):
    try:
        result = await aqua.read_user.perform(user_id)
    except Exception as error:
        return Error(unexpected_error=error)

    if result is None:
        return "no_user"

    target = result.target_water_balance_milliliters
    records = tuple(
        RecordData(
            record_id=record.record_id,
            drunk_water_milliliters=record.drunk_water_milliliters,
            recording_time=record.recording_time,
        )
        for record in result.records
    )
    return ReadUserOutputData(
        user_id=result.user_id,
        glass_milliliters=result.glass_milliliters,
        weight_kilograms=result.weight_kilograms,
        date_=result.date_,
        target_water_balance_milliliters=target,
        water_balance_milliliters=result.water_balance_milliliters,
        result_code=result.result_code,
        real_result_code=result.real_result_code,
        is_result_pinned=result.is_result_pinned,
        records=records,
    )


@dataclass(kw_only=True, frozen=True, slots=True)
class CancelRecordOutputData:
    user_id: UUID
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    cancelled_record: RecordData
    other_records: tuple[RecordData, ...]


@asynccontextmanager
async def cancel_record(
    user_id: UUID, record_id: UUID
) -> AsyncIterator[
    CancelRecordOutputData
    | Error
    | Literal["no_record"]
]:
    try:
        async with aqua.cancel_record.perform(user_id, record_id) as result:
            if result == "no_record":
                yield "no_record"
                return

            other_records = tuple(
                RecordData(
                    record_id=record.record_id,
                    drunk_water_milliliters=record.drunk_water_milliliters,
                    recording_time=record.recording_time,
                )
                for record in result.other_records
            )

            drunk_water = result.cancelled_record.drunk_water_milliliters
            cancelled_record = RecordData(
                record_id=result.cancelled_record.record_id,
                drunk_water_milliliters=drunk_water,
                recording_time=result.cancelled_record.recording_time,
            )

            target = result.target_water_balance_milliliters
            yield CancelRecordOutputData(
                user_id=result.user_id,
                date_=result.date_,
                target_water_balance_milliliters=target,
                water_balance_milliliters=result.water_balance_milliliters,
                result_code=result.result_code,
                real_result_code=result.real_result_code,
                is_result_pinned=result.is_result_pinned,
                cancelled_record=cancelled_record,
                other_records=other_records,
            )
    except Exception as error:
        yield Error(unexpected_error=error)

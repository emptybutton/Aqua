from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime, date
from typing import TypeVar, Generic, Literal
from uuid import UUID

from shared.application.ports.transactions import Transaction


_TransactionT_contra = TypeVar(
    "_TransactionT_contra",
    bound=Transaction,
    contravariant=True,
)


@dataclass(kw_only=True, frozen=True)
class RegisterUserOutput:
    user_id: UUID
    target_water_balance_milliliters: int
    glass_milliliters: int
    weight_kilograms: int | None


@dataclass(kw_only=True, frozen=True)
class WriteWaterOutput:
    user_id: UUID
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool
    date_: date

    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    previous_records: tuple[RecordData, ...]
    new_record: RecordData


@dataclass(kw_only=True, frozen=True)
class ReadDayOutput:
    user_id: UUID
    date_: date
    target_water_balance_milliliters: int
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool

    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    records: tuple[RecordData, ...]


@dataclass(kw_only=True, frozen=True)
class ReadUserOutput:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: int | None
    target_water_balance_milliliters: int
    date_: date
    water_balance_milliliters: int
    result_code: int
    real_result_code: int
    is_result_pinned: bool

    @dataclass(kw_only=True, frozen=True)
    class RecordData:
        record_id: UUID
        drunk_water_milliliters: int
        recording_time: datetime

    records: tuple[RecordData, ...]


class Aqua(Generic[_TransactionT_contra], ABC):
    @abstractmethod
    async def close(self) -> None: ...

    @abstractmethod
    async def register_user(
        self,
        auth_user_id: UUID,
        target_water_balance_milliliters: int | None,
        glass_milliliters: int | None,
        weight_kilograms: int | None,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        RegisterUserOutput
        | Literal["aqua_is_not_working"]
        | Literal["incorrect_water_amount"]
        | Literal["incorrect_weight_amount"]
        | Literal["no_weight_for_water_balance"]
        | Literal["extreme_weight_for_water_balance"]
    ): ...

    @abstractmethod
    async def write_water(
        self,
        user_id: UUID,
        milliliters: int | None,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        WriteWaterOutput
        | Literal["aqua_is_not_working"]
        | Literal["no_user"]
        | Literal["incorrect_water_amount"]
    ): ...

    @abstractmethod
    async def read_day(
        self,
        user_id: UUID,
        date_: date,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        ReadDayOutput | Literal["no_user"] | Literal["aqua_is_not_working"]
    ): ...

    @abstractmethod
    async def read_user(
        self,
        user_id: UUID,
        *,
        transaction: _TransactionT_contra,
    ) -> (
        ReadUserOutput | Literal["no_user"] | Literal["aqua_is_not_working"]
    ): ...

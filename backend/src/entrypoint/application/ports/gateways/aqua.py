from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, TypeVar, Generic
from uuid import UUID

from src.shared.application.ports.uows import UoW


@dataclass(frozen=True)
class RegistrationDTO:
    water_balance_milliliters: int
    glass_milliliters: int


@dataclass(frozen=True)
class WaterWritingDTO:
    record_id: UUID
    drunk_water_milliliters: int


@dataclass(frozen=True, kw_only=True)
class DayReadingDTO:
    target_water_balance: int
    real_water_balance: int
    result_code: int


@dataclass(frozen=True, kw_only=True)
class RecordDTO:
    id: UUID
    drunk_water: int
    recording_time: datetime


@dataclass(frozen=True, kw_only=True)
class DayRecordReadingDTO:
    records: tuple[RecordDTO, ...]


@dataclass(frozen=True, kw_only=True)
class UserDataReadingDTO:
    user_id: UUID
    glass_milliliters: int
    weight_kilograms: Optional[int]
    target_water_balance_milliliters: int


UoWT_contra = TypeVar("UoWT_contra", bound=UoW[object], contravariant=True)


class Gateway(Generic[UoWT_contra], ABC):
    @abstractmethod
    async def register_user(  # noqa: PLR0913
        self,
        auth_user_id: UUID,
        water_balance_milliliters: Optional[int],
        glass_milliliters: Optional[int],
        weight_kilograms: Optional[int],
        *,
        uow: UoWT_contra,
    ) -> RegistrationDTO: ...

    @abstractmethod
    async def write_water(
        self,
        auth_user_id: UUID,
        milliliters: Optional[int],
        *,
        uow: UoWT_contra,
    ) -> WaterWritingDTO: ...

    @abstractmethod
    async def read_day(
        self,
        user_id: UUID,
        date_: date,
        *,
        uow: UoWT_contra,
    ) -> DayReadingDTO: ...

    @abstractmethod
    async def read_day_records(
        self,
        user_id: UUID,
        date_: date,
        *,
        uow: UoWT_contra,
    ) -> DayRecordReadingDTO: ...

    @abstractmethod
    async def read_user_data(
        self,
        user_id: UUID,
        *,
        uow: UoWT_contra,
    ) -> Optional[UserDataReadingDTO]: ...

from abc import abstractmethod, ABC
from dataclasses import dataclass
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

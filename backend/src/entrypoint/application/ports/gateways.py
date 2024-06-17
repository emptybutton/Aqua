from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional, TypeVar
from uuid import UUID

from src.shared.application.ports.uows import UoW


@dataclass(frozen=True)
class AuthUserRegistrationDTO:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime


UoWT_contra = TypeVar("UoWT_contra", bound=UoW[object], contravariant=True)


class RegisterAuthUser(Protocol[UoWT_contra]):
    @abstractmethod
    async def __call__(
        self,
        name: str,
        password: str,
        *,
        uow: UoWT_contra,
    ) -> AuthUserRegistrationDTO: ...


@dataclass(frozen=True)
class AquaUserRegistrationDTO:
    water_balance_milliliters: int
    glass_milliliters: int


class RegisterAquaUser(Protocol[UoWT_contra]):
    @abstractmethod
    async def __call__(  # noqa: PLR0913
        self,
        auth_user_id: UUID,
        water_balance_milliliters: Optional[int],
        glass_milliliters: Optional[int],
        weight_kilograms: Optional[int],
        *,
        uow: UoWT_contra,
    ) -> AquaUserRegistrationDTO: ...


@dataclass(frozen=True)
class AuthUserAuthenticationDTO:
    auth_user_id: UUID


class AuthenticateAuthUser:
    @abstractmethod
    def __call__(self, jwt: str) -> AuthUserAuthenticationDTO: ...


@dataclass(frozen=True)
class WaterWritingDTO:
    record_id: UUID
    drunk_water_milliliters: int


class WriteWater(Protocol[UoWT_contra]):
    @abstractmethod
    async def __call__(
        self,
        auth_user_id: UUID,
        milliliters: Optional[int],
        *,
        uow: UoWT_contra,
    ) -> WaterWritingDTO: ...

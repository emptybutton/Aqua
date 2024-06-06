from abc import abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import Protocol, Optional, TypeVar

from src.shared.application.ports.uows import UoW


@dataclass(frozen=True)
class AuthUserRegistrationDTO:
    user_id: int
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


class RegisterAquaUser(Protocol[UoWT_contra]):
    @abstractmethod
    async def __call__(  # noqa: PLR0913
        self,
        auth_user_id: int,
        water_balance_milliliters: Optional[int],
        glass_milliliters: Optional[int],
        weight_kilograms: Optional[int],
        *,
        uow: UoWT_contra,
    ) -> object: ...

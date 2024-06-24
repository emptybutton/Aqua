from abc import abstractmethod, ABC
from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, Generic, Optional
from uuid import UUID

from src.shared.application.ports.uows import UoW


@dataclass(frozen=True)
class UserRegistrationDTO:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime


@dataclass(frozen=True)
class UserAuthenticationDTO:
    auth_user_id: UUID


@dataclass(frozen=True, kw_only=True)
class UserDataReadingDTO:
    username: str


UoWT_contra = TypeVar("UoWT_contra", bound=UoW[object], contravariant=True)


class Gateway(Generic[UoWT_contra], ABC):
    @abstractmethod
    async def register_user(
        self,
        name: str,
        password: str,
        *,
        uow: UoWT_contra,
    ) -> UserRegistrationDTO: ...

    @abstractmethod
    def authenticate_user(self, jwt: str) -> UserAuthenticationDTO: ...

    @abstractmethod
    async def read_user_data(
        self,
        user_id: UUID,
        *,
        uow: UoWT_contra,
    ) -> Optional[UserDataReadingDTO]: ...

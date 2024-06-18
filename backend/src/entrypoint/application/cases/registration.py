from dataclasses import dataclass
from datetime import datetime
from typing import TypeVar, Optional
from uuid import UUID

from src.entrypoint.application.ports import gateways
from src.shared.application.ports.uows import UoW


_UoWT = TypeVar("_UoWT", bound=UoW[object])


@dataclass(frozen=True)
class OutputDTO:
    user_id: UUID
    username: str
    access_token: str
    refresh_token: str
    refresh_token_expiration_date: datetime


async def register_user(  # noqa: PLR0913
    name: str,
    password: str,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    uow: _UoWT,
    auth_gateway: gateways.auth.Gateway[_UoWT],
    aqua_gateway: gateways.aqua.Gateway[_UoWT],
) -> OutputDTO:
    async with uow as uow:
        dto = await auth_gateway.register_user(name, password, uow=uow)
        auth_user_id = dto.user_id

        await aqua_gateway.register_user(
            auth_user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            uow=uow,
        )

        return OutputDTO(
            user_id=dto.user_id,
            username=dto.username,
            access_token=dto.access_token,
            refresh_token=dto.refresh_token,
            refresh_token_expiration_date=dto.refresh_token_expiration_date,
        )

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
    water_balance_milliliters: int
    glass_milliliters: int


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
        auth_result = await auth_gateway.register_user(name, password, uow=uow)
        auth_user_id = auth_result.user_id
        refresh_token_expiration = auth_result.refresh_token_expiration_date

        aqua_result = await aqua_gateway.register_user(
            auth_user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            uow=uow,
        )


        return OutputDTO(
            user_id=auth_result.user_id,
            username=auth_result.username,
            access_token=auth_result.access_token,
            refresh_token=auth_result.refresh_token,
            refresh_token_expiration_date=refresh_token_expiration,
            water_balance_milliliters=aqua_result.water_balance_milliliters,
            glass_milliliters=aqua_result.glass_milliliters,
        )

from dataclasses import dataclass
from typing import Optional, TypeVar
from uuid import UUID

from entrypoint.application.ports import gateways
from shared.application.ports.uows import UoW


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    username: str
    glass_milliliters: int
    target_water_balance_milliliters: int
    weight_kilograms: Optional[int]


_UoWT = TypeVar("_UoWT", bound=UoW[object])


async def read_user_data(
    jwt: str,
    *,
    uow: _UoWT,
    auth_gateway: gateways.auth.Gateway[_UoWT],
    aqua_gateway: gateways.aqua.Gateway[_UoWT],
) -> Optional[OutputDTO]:
    authentication_result = auth_gateway.authenticate_user(jwt)
    user_id = authentication_result.auth_user_id

    aqua_user_reading_result = await aqua_gateway.read_user_data(
        user_id,
        uow=uow,
    )

    if aqua_user_reading_result is None:
        return None

    auth_user_reading_result = await auth_gateway.read_user_data(
        user_id,
        uow=uow,
    )

    if auth_user_reading_result is None:
        return None

    water_balance = aqua_user_reading_result.target_water_balance_milliliters

    return OutputDTO(
        user_id=user_id,
        username=auth_user_reading_result.username,
        glass_milliliters=aqua_user_reading_result.glass_milliliters,
        target_water_balance_milliliters=water_balance,
        weight_kilograms=aqua_user_reading_result.weight_kilograms,
    )

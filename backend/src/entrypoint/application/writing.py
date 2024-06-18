from dataclasses import dataclass
from typing import TypeVar, Optional
from uuid import UUID

from src.entrypoint.application.ports import gateways
from src.shared.application.ports.uows import UoW


_UoWT = TypeVar("_UoWT", bound=UoW[object])


@dataclass(frozen=True, kw_only=True)
class OutputDTO:
    user_id: UUID
    record_id: UUID
    drunk_water_milliliters: int


async def write_water(
    jwt: str,
    milliliters: Optional[int],
    *,
    authenticate_auth_user: gateways.AuthenticateAuthUser,
    write_water: gateways.WriteWater[_UoWT],
    uow: _UoWT,
) -> OutputDTO:
    authentication_result = authenticate_auth_user(jwt)
    writing_result = await write_water(
        authentication_result.auth_user_id,
        milliliters,
        uow=uow,
    )

    return OutputDTO(
        user_id=authentication_result.auth_user_id,
        record_id=writing_result.record_id,
        drunk_water_milliliters=writing_result.drunk_water_milliliters,
    )

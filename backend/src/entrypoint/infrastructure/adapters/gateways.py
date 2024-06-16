from typing import Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncConnection

from src.auth.presentation.adapters import (
    registration as auth_registration,
    authentication,
)
from src.aqua.presentation.adapters import (
    registration as aqua_registration,
    writing,
)
from src.entrypoint.application.ports import gateways
from src.shared.application.ports.uows import UoW


register_auth_user: gateways.RegisterAuthUser[UoW[object]]
async def register_auth_user(  # type: ignore[no-redef]
    name: str,
    password: str,
    *,
    uow: object,  # noqa: ARG001
    connection: AsyncConnection,
) -> gateways.AuthUserRegistrationDTO:
    result = await auth_registration.register_user(
        name,
        password,
        connection=connection,
    )

    return gateways.AuthUserRegistrationDTO(
        user_id=result.user_id,
        username=result.username,
        access_token=result.serialized_access_token,
        refresh_token_expiration_date=result.refresh_token_expiration_date,
        refresh_token=result.refresh_token_text,
    )


async def register_aqua_user(  # noqa: PLR0913
    auth_user_id: UUID,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    uow: object,  # noqa: ARG001
    connection: AsyncConnection,
) -> None:
    await aqua_registration.register_user(
        auth_user_id,
        water_balance_milliliters,
        glass_milliliters,
        weight_kilograms,
        connection=connection,
    )


async def write_water(
    auth_user_id: UUID,
    milliliters: Optional[int],
    *,
    uow: object,  # noqa: ARG001
    connection: AsyncConnection,
) -> gateways.WaterWritingDTO:
    result = await writing.write_water(
        auth_user_id,
        milliliters,
        connection=connection,
    )

    return gateways.WaterWritingDTO(
        record_id=result.record_id,
        drunk_water_milliliters=result.drunk_water_milliliters,
    )


authenticate_auth_user: gateways.AuthenticateAuthUser
def authenticate_auth_user(jwt: str) -> gateways.AuthUserAuthenticationDTO:  # type: ignore[no-redef]
    result = authentication.authenticate_user(jwt)

    return gateways.AuthUserAuthenticationDTO(
        auth_user_id=result.user_id
    )

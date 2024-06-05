from typing import TypeVar, Optional

from src.entrypoint.application.ports import actions
from src.shared.application.ports.uows import UoW


_UoWT = TypeVar("_UoWT", bound=UoW[object])


async def register_user(  # noqa: PLR0913
    name: str,
    password: str,
    water_balance_milliliters: Optional[int],
    glass_milliliters: Optional[int],
    weight_kilograms: Optional[int],
    *,
    uow: _UoWT,
    register_auth_user: actions.RegisterAuthUser[_UoWT],
    register_aqua_user: actions.RegisterAquaUser[_UoWT],
) -> None:
    async with uow as uow:
        dto = await register_auth_user(name, password, uow=uow)
        auth_user_id = dto.user_id

        await register_aqua_user(
            auth_user_id,
            water_balance_milliliters,
            glass_milliliters,
            weight_kilograms,
            uow=uow,
        )

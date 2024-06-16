from typing import Optional, TypeAlias
from functools import partial

from sqlalchemy.ext.asyncio import AsyncEngine

from src.entrypoint.application import writing
from src.entrypoint.infrastructure.adapters import gateways
from src.shared.infrastructure.adapters import uows


OutputDTO: TypeAlias = writing.OutputDTO


async def write_water(
    jwt: str,
    milliliters: Optional[int],
    *,
    engine: AsyncEngine,
) -> OutputDTO:
    async with engine.connect() as connection:
        write_water = partial(
            gateways.write_water,
            connection=connection,
        )

        return await writing.write_water(
            jwt,
            milliliters,
            authenticate_auth_user=gateways.authenticate_auth_user,
            write_water=write_water,
            uow=uows.FakeUoW(),
        )

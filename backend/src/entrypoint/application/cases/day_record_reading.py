from datetime import date
from typing import TypeVar, TypeAlias

from src.entrypoint.application.ports import gateways
from src.shared.application.ports.uows import UoW


_UoWT = TypeVar("_UoWT", bound=UoW[object])


OutputDTO: TypeAlias = gateways.aqua.DayRecordReadingDTO

RecordDTO: TypeAlias = gateways.aqua.RecordDTO


async def read_day_records(
    jwt: str,
    date_: date,
    *,
    uow: _UoWT,
    auth_gateway: gateways.auth.Gateway[_UoWT],
    aqua_gateway: gateways.aqua.Gateway[_UoWT],
) -> OutputDTO:
    authentication_result = auth_gateway.authenticate_user(jwt)

    return await aqua_gateway.read_day_records(
        authentication_result.auth_user_id,
        date_,
        uow=uow,
    )

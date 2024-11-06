from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID

from entrypoint.application import ports
from entrypoint.application.cases import rename_user
from entrypoint.infrastructure.adapters import clients
from entrypoint.presentation.di.containers import sync_container


@dataclass(kw_only=True, frozen=True)
class OkOtherData:
    new_username: str
    previous_username: str


OtherData: TypeAlias = (
    OkOtherData
    | Literal["error"]
    | Literal["new_username_taken"]
    | Literal["empty_new_username"]
)


@dataclass(kw_only=True, frozen=True)
class OutputData:
    user_id: UUID
    session_id: UUID
    other_data: OtherData


Output: TypeAlias = OutputData | Literal["error"] | Literal["not_authenticated"]


async def perform(session_id: UUID, new_username: str) -> Output:
    with sync_container() as container:
        result = await rename_user.perform(
            session_id,
            new_username,
            auth=await container.get(clients.auth.AuthFacade, "clients"),
            auth_logger=await container.get(
                ports.loggers.AuthLogger[clients.auth.AuthFacade], "loggers"
            ),
        )

    if not isinstance(result, rename_user.OutputData):
        return result

    other_data: OtherData

    if isinstance(result.renaming_output, ports.clients.auth.RenameUserOutput):
        other_data = OkOtherData(
            new_username=result.renaming_output.new_username,
            previous_username=result.renaming_output.previous_username,
        )
    else:
        other_data = result.renaming_output

    return OutputData(
        user_id=result.authentication_output.user_id,
        session_id=result.authentication_output.session_id,
        other_data=other_data,
    )

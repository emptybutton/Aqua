from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from entrypoint.infrastructure.facades.clients import aqua, auth
from entrypoint.infrastructure.facades.loggers import aqua_logger, auth_logger
from entrypoint.logic.tools.context import Context, finalize_bad


@dataclass(kw_only=True, frozen=True)
class OutputData:
    auth_output: auth.RegisterUserOutputData
    aqua_output: aqua.RegisterUserOutputData


type Output = (
    OutputData
    | Literal["error"]
    | Literal["incorrect_water_amount"]
    | Literal["incorrect_weight_amount"]
    | Literal["no_weight_for_water_balance"]
    | Literal["extreme_weight_for_water_balance"]
    | Literal["taken_username"]
    | Literal["empty_username"]
    | Literal["week_password"]
)


async def register_user(
    session_id: UUID | None,
    name: str,
    password: str,
    target_water_balance_milliliters: int | None,
    glass_milliliters: int | None,
    weight_kilograms: int | None,
) -> Output:
    auth_context = Context(auth.register_user(session_id, name, password))
    async with auth_context as auth_result:
        if not isinstance(auth_result, auth.RegisterUserOutputData):
            if isinstance(auth_result, auth.Error):
                await auth_logger.log_error(auth_result)
                return "error"

            return auth_result

        aqua_context = Context(
            aqua.register_user(
                auth_result.user_id,
                target_water_balance_milliliters,
                glass_milliliters,
                weight_kilograms,
            )
        )
        async with aqua_context as aqua_result:
            if not isinstance(aqua_result, aqua.RegisterUserOutputData):
                await finalize_bad(auth_context)

                if isinstance(aqua_result, aqua.Error):
                    await aqua_logger.log_error(aqua_result)
                    return "error"

            return OutputData(auth_output=auth_result, aqua_output=aqua_result)

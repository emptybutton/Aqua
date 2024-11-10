from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.register_user import register_user as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import (
    optional_valid_id_of,
)
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.bad.empty_username import (
    empty_username_response_model,
)
from entrypoint.presentation.fastapi.views.bad.extreme_weight_for_water_balance import (  # noqa: E501
    extreme_weight_for_water_balance_response_model,
)
from entrypoint.presentation.fastapi.views.bad.fault import fault_response_model
from entrypoint.presentation.fastapi.views.bad.invalid_session_id_hex import (
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.bad.invalid_water_amount import (
    invalid_water_amount_response_model,
)
from entrypoint.presentation.fastapi.views.bad.invalid_weight_amount import (
    invalid_weight_amount_response_model,
)
from entrypoint.presentation.fastapi.views.bad.no_weight_for_water_balance import (  # noqa: E501
    no_weight_for_water_balance_response_model,
)
from entrypoint.presentation.fastapi.views.bad.taken_username import (
    taken_username_response_model,
)
from entrypoint.presentation.fastapi.views.bad.week_password import (
    week_password_response_model,
)
from entrypoint.presentation.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.cookies import SessionCookie
from entrypoint.presentation.fastapi.views.ok.user.registered_user import (
    RegisteredUserSchema,
    registered_user_response_model,
)


class RegisterUserRequestModel(BaseModel):
    username: str
    password: str
    target_water_balance_milliliters: int | None = None
    glass_milliliters: int | None = None
    weight_kilograms: int | None = None


@router.post(
    "/user/register",
    tags=[Tag.access_endpoints],
    status_code=registered_user_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        invalid_session_id_hex_response_model,
        invalid_water_amount_response_model,
        invalid_weight_amount_response_model,
        no_weight_for_water_balance_response_model,
        extreme_weight_for_water_balance_response_model,
        taken_username_response_model,
        empty_username_response_model,
        week_password_response_model,
        registered_user_response_model,
    ),
)
async def register_user(
    request_model: RegisterUserRequestModel,
    session_id_hex: cookies.optional_session_id_cookie,
) -> Response:
    session_id = optional_valid_id_of(session_id_hex)

    if session_id == "invalid_hex":
        return invalid_session_id_hex_response_model.to_response()

    result = await service(
        session_id,
        request_model.username,
        request_model.password,
        request_model.target_water_balance_milliliters,
        request_model.glass_milliliters,
        request_model.weight_kilograms,
    )

    if result == "error":
        return fault_response_model.to_response()

    if result == "incorrect_weight_amount":
        return invalid_weight_amount_response_model.to_response()

    if result == "incorrect_water_amount":
        return invalid_water_amount_response_model.to_response()

    if result == "extreme_weight_for_water_balance":
        return extreme_weight_for_water_balance_response_model.to_response()

    if result == "no_weight_for_water_balance":
        return no_weight_for_water_balance_response_model.to_response()

    if result == "taken_username":
        return taken_username_response_model.to_response()

    if result == "empty_username":
        return empty_username_response_model.to_response()

    if result == "week_password":
        return week_password_response_model.to_response()

    target = result.aqua_output.target_water_balance_milliliters
    body = RegisteredUserSchema(
        user_id=result.auth_output.user_id,
        username=result.auth_output.username,
        target_water_balance_milliliters=target,
        glass_milliliters=result.aqua_output.glass_milliliters,
        weight_kilograms=result.aqua_output.weight_kilograms,
    )
    response = registered_user_response_model.to_response(body)

    session_cookie = SessionCookie(response)
    session_cookie.set(result.auth_output.new_session_id)

    return response

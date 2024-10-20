from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class RegisterUserRequestModel(BaseModel):
    username: str
    password: str
    target_water_balance_milliliters: int | None = None
    glass_milliliters: int | None = None
    weight_kilograms: int | None = None


@router.post(
    "/user/register",
    tags=[Tag.access_endpoints],
    status_code=views.responses.ok.registered_user_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.incorrect_water_amount_view,
        views.responses.bad.incorrect_weight_amount_view,
        views.responses.bad.no_weight_for_water_balance_view,
        views.responses.bad.extreme_weight_for_water_balance_view,
        views.responses.bad.user_is_already_registered_view,
        views.responses.bad.empty_username_view,
        views.responses.bad.week_password_view,
        views.responses.ok.registered_user_view,
    ),
)
async def register_user(
    request_model: RegisterUserRequestModel,
    session_id_hex: cookies.optional_session_id_cookie,
) -> Response:
    result = await facade.register_user.perform(
        id_of(session_id_hex),
        request_model.username,
        request_model.password,
        request_model.target_water_balance_milliliters,
        request_model.glass_milliliters,
        request_model.weight_kilograms,
    )

    if result == "not_working":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "incorrect_weight_amount":
        return views.responses.bad.incorrect_weight_amount_view.to_response()

    if result == "incorrect_water_amount":
        return views.responses.bad.incorrect_water_amount_view.to_response()

    if result == "extreme_weight_for_water_balance":
        weight_view = views.responses.bad.extreme_weight_for_water_balance_view
        return weight_view.to_response()

    if result == "no_weight_for_water_balance":
        water_balance_view = (
            views.responses.bad.no_weight_for_water_balance_view
        )
        return water_balance_view.to_response()

    if result == "user_is_already_registered":
        return views.responses.bad.user_is_already_registered_view.to_response()

    if result == "empty_username":
        return views.responses.bad.empty_username_view.to_response()

    if result == "week_password":
        return views.responses.bad.week_password_view.to_response()

    target = result.target_water_balance_milliliters
    body = views.bodies.ok.RegisteredUserView(
        user_id=result.user_id,
        username=result.username,
        target_water_balance_milliliters=target,
        glass_milliliters=result.glass_milliliters,
        weight_kilograms=result.weight_kilograms,
    )
    response = views.responses.ok.registered_user_view.to_response(body)

    session_cookie = views.cookies.SessionCookie(response)
    session_cookie.set(result.session_id)

    return response

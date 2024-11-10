from fastapi import Response

from entrypoint.logic.services.read_user import read_user as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import valid_id_of
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.bad.fault import fault_response_model
from entrypoint.presentation.fastapi.views.bad.invalid_session_id_hex import (
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.bad.not_authenticated import (
    not_authenticated_response_model,
)
from entrypoint.presentation.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.common.record import RecordSchema
from entrypoint.presentation.fastapi.views.ok.user.user import (
    UserSchema,
    UserSchemaFirstPart,
    UserSchemaSecondPart,
    user_response_model,
)


@router.get(
    "/user",
    tags=[Tag.current_user_endpoints],
    status_code=user_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        invalid_session_id_hex_response_model,
        not_authenticated_response_model,
        user_response_model,
    ),
)
async def read_user(session_id_hex: cookies.session_id_cookie) -> Response:
    session_id = valid_id_of(session_id_hex)

    if session_id is None:
        return not_authenticated_response_model.to_response()

    result = await service(session_id)

    if result == "error":
        return fault_response_model.to_response()

    if result == "not_authenticated":
        return not_authenticated_response_model.to_response()

    if result.auth_output is None:
        first_part = None
    else:
        first_part = UserSchemaFirstPart(username=result.first_part.username)

    if result.aqua_output is None:
        second_part = None
    else:
        records = tuple(map(RecordSchema.of, result.aqua_output.second_part))

        target = result.aqua_output.target_water_balance_milliliters
        second_part = UserSchemaSecondPart(
            glass_milliliters=result.aqua_output.glass_milliliters,
            weight_kilograms=result.aqua_output.weight_kilograms,
            target_water_balance_milliliters=target,
            date_=result.aqua_output.date_,
            water_balance_milliliters=result.aqua_output.water_balance_milliliters,
            result_code=result.aqua_output.result_code,
            real_result_code=result.aqua_output.real_result_code,
            is_result_pinned=result.aqua_output.is_result_pinned,
            records=records,
        )

    body = UserSchema(
        user_id=result.authentication_output.user_id,
        first_part=first_part,
        second_part=second_part,
    )
    return user_response_model.to_response(body)

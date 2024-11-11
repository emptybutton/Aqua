
from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.write_water import write_water as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import valid_id_of
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.responses.bad.fault import (
    fault_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_session_id_hex import (  # noqa: E501
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.invalid_water_amount import (  # noqa: E501
    invalid_water_amount_response_model,
)
from entrypoint.presentation.fastapi.views.responses.bad.not_authenticated import (  # noqa: E501
    not_authenticated_response_model,
)
from entrypoint.presentation.fastapi.views.responses.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.responses.common.record import (
    RecordSchema,
)
from entrypoint.presentation.fastapi.views.responses.ok.record.new_record import (  # noqa: E501
    NewRecordSchema,
    new_record_response_model,
)


class CreateRecordRequestModel(BaseModel):
    water_milliliters: int | None = None


@router.post(
    "/user/records",
    tags=[Tag.current_user_endpoints],
    status_code=new_record_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        not_authenticated_response_model,
        invalid_session_id_hex_response_model,
        new_record_response_model,
    ),
)
async def create_record(
    request_model: CreateRecordRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = valid_id_of(session_id_hex)

    if session_id is None:
        return invalid_session_id_hex_response_model.to_response()

    result = await service(session_id, request_model.water_milliliters)

    if result == "error":
        return fault_response_model.to_response()

    if result == "not_authenticated":
        return not_authenticated_response_model.to_response()

    if result.aqua_output == "error":
        return fault_response_model.to_response()

    if result.aqua_output == "incorrect_water_amount":
        return invalid_water_amount_response_model.to_response()

    target_water_balance_milliliters = (
        result.aqua_output.target_water_balance_milliliters
    )
    body = NewRecordSchema(
        user_id=result.aqua_output.user_id,
        target_water_balance_milliliters=target_water_balance_milliliters,
        water_balance_milliliters=result.aqua_output.water_balance_milliliters,
        result_code=result.aqua_output.result_code,
        real_result_code=result.aqua_output.real_result_code,
        is_result_pinned=result.aqua_output.is_result_pinned,
        date_=result.aqua_output.date_,
        previous_records=(
            tuple(map(RecordSchema.of, result.aqua_output.previous_records))
        ),
        new_record=RecordSchema.of(result.aqua_output.new_record),
    )

    return new_record_response_model.to_response(body)

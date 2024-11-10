from uuid import UUID

from fastapi import Response
from pydantic import BaseModel

from entrypoint.logic.services.cancel_record import cancel_record as service
from entrypoint.presentation.fastapi.controllers import cookies
from entrypoint.presentation.fastapi.controllers.parsers import valid_id_of
from entrypoint.presentation.fastapi.controllers.routers import router
from entrypoint.presentation.fastapi.controllers.tags import Tag
from entrypoint.presentation.fastapi.views.bad.fault import fault_response_model
from entrypoint.presentation.fastapi.views.bad.invalid_session_id_hex import (
    invalid_session_id_hex_response_model,
)
from entrypoint.presentation.fastapi.views.bad.no_record import (
    no_record_response_model,
)
from entrypoint.presentation.fastapi.views.bad.not_authenticated import (
    not_authenticated_response_model,
)
from entrypoint.presentation.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.fastapi.views.common.record import RecordSchema
from entrypoint.presentation.fastapi.views.ok.record.cancelled_record import (
    CancelledRecordSchema,
    cancelled_record_response_model,
)


class CancelRecordRequestModel(BaseModel):
    record_id: UUID


@router.delete(
    "/user/records",
    tags=[Tag.current_user_endpoints],
    status_code=cancelled_record_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        invalid_session_id_hex_response_model,
        not_authenticated_response_model,
        cancelled_record_response_model,
    ),
)
async def cancel_record(
    request_model: CancelRecordRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = valid_id_of(session_id_hex)

    if session_id is None:
        return invalid_session_id_hex_response_model.to_response()

    result = await service(session_id, request_model.record_id)

    if result == "error":
        return fault_response_model.to_response()

    if result == "not_authenticated":
        return not_authenticated_response_model.to_response()

    if result.aqua_output == "error":
        return fault_response_model.to_response()

    if result.aqua_output == "no_record":
        return no_record_response_model.to_response()

    target = result.aqua_output.target_water_balance_milliliters
    body = CancelledRecordSchema(
        user_id=result.aqua_output.user_id,
        target_water_balance_milliliters=target,
        date_=result.aqua_output.date_,
        water_balance_milliliters=result.aqua_output.water_balance_milliliters,
        result_code=result.aqua_output.result_code,
        real_result_code=result.aqua_output.real_result_code,
        is_result_pinned=result.aqua_output.is_result_pinned,
        cancelled_record=RecordSchema.of(result.aqua_output.cancelled_record),
        other_records=(
            tuple(map(RecordSchema.of, result.aqua_output.other_records))
        ),
    )

    return cancelled_record_response_model.to_response(body)

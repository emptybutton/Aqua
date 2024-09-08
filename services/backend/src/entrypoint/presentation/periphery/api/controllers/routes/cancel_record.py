from uuid import UUID

from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class CancelRecordRequestModel(BaseModel):
    record_id: UUID


@router.delete(
    "/user/records",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.cancelled_record_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.cancelled_record_view,
    ),
)
async def cancel_record(
    request_model: CancelRecordRequestModel,
    session_id: cookies.session_id_cookie,
) -> Response:
    result = await facade.cancel_record.perform(
        session_id, request_model.record_id
    )

    if result == "error":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    data: views.bodies.ok.CancelledRecordView.Data = None
    error: views.bodies.ok.CancelledRecordView.Error = None

    if result.data == "error":
        error = "unexpected_error"
    elif result.data == "no_record":
        error = "no_record"
    else:
        drunk_water = result.data.cancelled_record.drunk_water_milliliters
        cancelled_record = views.bodies.ok.RecordView(
            record_id=result.data.cancelled_record.record_id,
            drunk_water_milliliters=drunk_water,
            recording_time=result.data.cancelled_record.recording_time,
        )
        day_records = tuple(
            views.bodies.ok.RecordView(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.data.day_records
        )
        target = result.data.target_water_balance_milliliters
        data = views.bodies.ok.CancelledRecordView.OkData(
            target_water_balance_milliliters=target,
            water_balance_milliliters=result.data.water_balance_milliliters,
            result_code=result.data.result_code,
            real_result_code=result.data.real_result_code,
            is_result_pinned=result.data.is_result_pinned,
            date_=result.data.date_,
            day_records=day_records,
            cancelled_record=cancelled_record,
        )

    body = views.bodies.ok.CancelledRecordView(
        user_id=result.user_id,
        data=data,
        error=error,
    )
    return views.responses.ok.cancelled_record_view.to_response(body)

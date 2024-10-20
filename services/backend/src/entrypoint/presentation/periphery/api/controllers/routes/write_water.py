from typing import Literal

from fastapi import Response
from pydantic import BaseModel

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


class CreateRecordRequestModel(BaseModel):
    water_milliliters: int | None = None


@router.post(
    "/user/records",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.new_record_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.new_record_view,
    ),
)
async def create_record(
    request_model: CreateRecordRequestModel,
    session_id_hex: cookies.session_id_cookie,
) -> Response:
    session_id = id_of(session_id_hex)

    if session_id is None:
        return views.responses.bad.not_authenticated_view.to_response()

    result = await facade.write_water.perform(
        session_id,
        request_model.water_milliliters,
    )

    if result == "not_working":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    data: (
        views.bodies.ok.NewRecordView.Data
        | Literal["incorrect_water_amount"]
        | None
    )

    if result.other == "error":
        data = None
    elif result.other == "incorrect_water_amount":
        data = "incorrect_water_amount"
    else:
        new_record = views.bodies.ok.RecordView(
            record_id=result.other.new_record.record_id,
            drunk_water_milliliters=result.other.new_record.drunk_water_milliliters,
            recording_time=result.other.new_record.recording_time,
        )
        previous_records = tuple(
            views.bodies.ok.RecordView(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.other.previous_records
        )
        target = result.other.target_water_balance_milliliters
        data = views.bodies.ok.NewRecordView.Data(
            target_water_balance_milliliters=target,
            water_balance_milliliters=result.other.water_balance_milliliters,
            result_code=result.other.result_code,
            real_result_code=result.other.real_result_code,
            is_result_pinned=result.other.is_result_pinned,
            date_=result.other.date_,
            previous_records=previous_records,
            new_record=new_record,
        )

    body = views.bodies.ok.NewRecordView(user_id=result.user_id, data=data)
    return views.responses.ok.new_record_view.to_response(body)

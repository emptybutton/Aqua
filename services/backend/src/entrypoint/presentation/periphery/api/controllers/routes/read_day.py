from datetime import date

from fastapi import Response

from entrypoint.presentation.di import facade
from entrypoint.presentation.periphery.api import views
from entrypoint.presentation.periphery.api.controllers import cookies
from entrypoint.presentation.periphery.api.controllers.parsers import id_of
from entrypoint.presentation.periphery.api.controllers.routers import router
from entrypoint.presentation.periphery.api.controllers.tags import Tag


@router.get(
    "/user/day",
    tags=[Tag.current_user_endpoints],
    status_code=views.responses.ok.day_view.status_code,
    responses=views.responses.common.to_doc(
        views.responses.bad.backend_is_not_working_view,
        views.responses.bad.not_authenticated_view,
        views.responses.ok.day_view,
    ),
)
async def read_day(
    session_id_hex: cookies.session_id_cookie,
    date_: date,
) -> Response:
    session_id = id_of(session_id_hex)

    if session_id is None:
        return views.responses.bad.not_authenticated_view.to_response()

    result = await facade.read_day.perform(
        session_id,
        date_,
    )

    if result == "not_working":
        return views.responses.bad.backend_is_not_working_view.to_response()

    if result == "not_authenticated":
        return views.responses.bad.not_authenticated_view.to_response()

    if result.other is None:
        data = None
    else:
        records = tuple(
            views.bodies.ok.RecordView(
                record_id=record.record_id,
                drunk_water_milliliters=record.drunk_water_milliliters,
                recording_time=record.recording_time,
            )
            for record in result.other.records
        )
        target = result.other.target_water_balance_milliliters
        data = views.bodies.ok.DayView.Data(
            target_water_balance_milliliters=target,
            date_=result.other.date_,
            water_balance_milliliters=result.other.water_balance_milliliters,
            result_code=result.other.result_code,
            real_result_code=result.other.real_result_code,
            is_result_pinned=result.other.is_result_pinned,
            records=records,
        )

    body = views.bodies.ok.DayView(user_id=result.user_id, data=data)
    return views.responses.ok.day_view.to_response(body)

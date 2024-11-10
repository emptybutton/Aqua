from fastapi import Response

from entrypoint.presentation.logic.services.user_exists import (
    user_exists as service,
)
from entrypoint.presentation.periphery.fastapi.controllers.routers import router
from entrypoint.presentation.periphery.fastapi.controllers.tags import Tag
from entrypoint.presentation.periphery.fastapi.views.bad.fault import (
    fault_response_model,
)
from entrypoint.presentation.periphery.fastapi.views.common.model import (
    to_doc,
)
from entrypoint.presentation.periphery.fastapi.views.ok.user.user_exists import (  # noqa: E501
    UserExistsSchema,
    user_exists_response_model,
)


@router.get(
    "/user/exists",
    tags=[Tag.other_users_endpoints],
    status_code=user_exists_response_model.status_code,
    responses=to_doc(
        fault_response_model,
        user_exists_response_model,
    ),
)
async def user_exists(username: str) -> Response:
    result = await service(username)

    if result == "error":
        return fault_response_model.to_response()

    body = UserExistsSchema(exists=result)
    return user_exists_response_model.to_response(body)

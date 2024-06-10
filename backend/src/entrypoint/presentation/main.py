from typing import Callable, Awaitable

from fastapi import FastAPI, Request, Response

from src.entrypoint.presentation.routes import router
from src.entrypoint.presentation.error_responses import for_api


app = FastAPI()


@app.middleware("http")
async def error_handler_middleware(
    request: Request,
    call_next: Callable[[Request], Awaitable[Response]],
) -> Response:
    try:
        return await call_next(request)
    except Exception as error:
        raise for_api(error) from error


app.include_router(router)

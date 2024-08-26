from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import FastAPI

from entrypoint.presentation.di.facade import close
from entrypoint.presentation.periphery.api.controllers.routes import router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa: ARG001
    yield
    await close.perform()


description = (
    "Aqua is an open source application for tracking your water balance,"
    " published on [github](https://github.com/emptybutton/Aqua)."
)

app = FastAPI(
    title="AquaAPI",
    version="0.1.0",
    summary="Main API for interaction with Aqua.",
    description=description,
    contact={
        "name": "Alexander Smolin",
        "url": "https://github.com/emptybutton",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://github.com/emptybutton/Aqua/blob/main/LICENSE",
    },
    lifespan=lifespan,
)
app.include_router(router)

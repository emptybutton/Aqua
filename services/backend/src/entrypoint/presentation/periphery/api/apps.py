from contextlib import asynccontextmanager
from typing import AsyncIterable

from fastapi import FastAPI

from entrypoint.presentation.di.facade import close
from entrypoint.presentation.periphery.api.controllers.routes import router


@asynccontextmanager
async def lifespan() -> AsyncIterable:
    yield
    await close.perform()


app = FastAPI(lifespan=lifespan)
app.include_router(router)

from typing import AsyncIterator

from httpx import ASGITransport, AsyncClient
from pytest import fixture

from entrypoint.presentation.fastapi.app import app


@fixture
async def client() -> AsyncIterator[AsyncClient]:
    client_ = AsyncClient(
        transport=ASGITransport(app=app), base_url="http://localhost"
    )

    async with client_:
        yield client_

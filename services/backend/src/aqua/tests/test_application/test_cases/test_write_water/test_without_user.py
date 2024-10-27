from uuid import uuid4

from pytest import mark
from result import Err

from aqua.application.cases.write_water import (
    NoUserError,
)
from aqua.tests.test_application.test_cases.test_write_water.conftest import (
    Context,
)


@mark.asyncio
async def test_result(context: Context) -> None:
    result = await context.write_water(uuid4(), None)

    assert result == Err(NoUserError())


@mark.asyncio
async def test_storage(context: Context) -> None:
    await context.write_water(uuid4(), None)

    assert not context.users


@mark.asyncio
async def test_logs(context: Context) -> None:
    await context.write_water(uuid4(), None)

    assert context.logger.is_empty

from uuid import UUID

from pytest import mark
from result import Err

from aqua.application.cases.register_user import (
    NegativeTargetWaterBalanceMillilitersError,
)
from aqua.tests.test_application.test_cases.test_register_user.conftest import (
    Context,
)


@mark.asyncio
async def test_result(context: Context) -> None:
    result = await context.register_user(UUID(int=1), -5000, 300, 70)

    assert result == Err(NegativeTargetWaterBalanceMillilitersError())


@mark.asyncio
async def test_storage(context: Context) -> None:
    await context.register_user(UUID(int=1), -5000, 300, 70)

    assert not tuple(context.users)


@mark.asyncio
async def test_logs(context: Context) -> None:
    await context.register_user(UUID(int=1), -5000, 300, 70)

    assert context.logger.is_empty

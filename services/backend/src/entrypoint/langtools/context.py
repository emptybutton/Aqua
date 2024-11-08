from types import TracebackType
from typing import Any, AsyncContextManager, Type


class BadFinalizationError(Exception): ...


class InactiveContextError(Exception): ...


class _NoValue: ...


_no_value = _NoValue()


class Context[EnterValueT]:
    __is_completed = False
    __enter_value: EnterValueT | _NoValue = _no_value

    def __init__(self, manager: AsyncContextManager[EnterValueT]) -> None:
        self.__manager = manager

    @property
    def enter_value(self) -> EnterValueT:
        if isinstance(self.__enter_value, _NoValue):
            raise InactiveContextError

        return self.__enter_value

    async def __finalize_bad__(self) -> None:  # noqa: PLW3201
        error = BadFinalizationError()
        await self.__manager.__aexit__(
            BadFinalizationError,
            error,
            error.__traceback__,
        )
        self.__is_completed = True

    async def __aenter__(self) -> EnterValueT:
        self.__enter_value = await self.__manager.__aenter__()

        return self.__enter_value

    async def __aexit__(
        self,
        error_type: Type[BaseException] | None,
        error: BaseException | None,
        traceback: TracebackType | None,
    ) -> bool | None:
        if self.__is_completed:
            self.__is_completed = False
            return None

        self.__enter_value = _no_value

        return await self.__manager.__aexit__(error_type, error, traceback)


async def finalize_bad(context: Context[Any]) -> None:
    await context.__finalize_bad__()

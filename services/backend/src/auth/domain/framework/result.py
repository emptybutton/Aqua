from typing import Awaitable, Callable, Concatenate

from result import Err, Ok, Result


def swap[V, E](result: Result[V, E]) -> Result[E, V]:
    match result:
        case Ok(v):
            return Err(v)
        case Err(e):
            return Ok(e)


def ok[**Params, ValueT](
    act: Callable[Params, ValueT],
) -> Callable[Params, Ok[ValueT]]:
    def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> Ok[ValueT]:
        return Ok(act(*args, **kwargs))

    return wrapper


def from_[AValueT, AErrorT, BValueT, BErrorT, **Params](
    result: Result[AValueT, AErrorT],
) -> Callable[
    [Callable[Concatenate[AValueT, Params], Result[BValueT, BErrorT]]],
    Callable[Params, Result[BValueT, AErrorT | BErrorT]],
]:
    def decorator(
        act: Callable[Concatenate[AValueT, Params], Result[BValueT, BErrorT]],
    ) -> Callable[Params, Result[BValueT, AErrorT | BErrorT]]:
        def wrapper(
            *args: Params.args, **kwargs: Params.kwargs
        ) -> Result[BValueT, AErrorT | BErrorT]:
            return result.and_then(lambda value: act(value, *args, **kwargs))

        return wrapper

    return decorator


def async_from[AValueT, AErrorT, BValueT, BErrorT, **Params](
    result: Result[AValueT, AErrorT],
) -> Callable[
    [
        Callable[
            Concatenate[AValueT, Params], Awaitable[Result[BValueT, BErrorT]]
        ]
    ],
    Callable[Params, Awaitable[Result[BValueT, AErrorT | BErrorT]]],
]:
    def decorator(
        act: Callable[
            Concatenate[AValueT, Params], Awaitable[Result[BValueT, BErrorT]]
        ],
    ) -> Callable[Params, Awaitable[Result[BValueT, AErrorT | BErrorT]]]:
        async def wrapper(
            *args: Params.args, **kwargs: Params.kwargs
        ) -> Result[BValueT, AErrorT | BErrorT]:
            return await result.and_then_async(
                lambda value: act(value, *args, **kwargs)
            )

        return wrapper

    return decorator


async def sync[ValueT, ErrorT](
    async_result: Result[Awaitable[ValueT], ErrorT],
) -> Result[ValueT, ErrorT]:
    return await async_result.map_async(lambda value: value)

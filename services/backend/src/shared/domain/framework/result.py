from functools import wraps
from typing import Callable, Concatenate, cast

from result import Err, Ok, Result, is_ok


def swap[V, E](result: Result[V, E]) -> Result[E, V]:
    if is_ok(result):
        return Err(result.ok())

    return Ok(cast(Err[E], result).err())


def ok[**Params, ValueT](
    act: Callable[Params, ValueT]
) -> Callable[Params, Ok[ValueT]]:
    @wraps(act)
    def wrapper(*args: Params.args, **kwargs: Params.kwargs) -> Ok[ValueT]:
        return Ok(act(*args, **kwargs))

    return wrapper


def frm[
    AValueT,
    AErrorT,
    BValueT,
    BErrorT,
    **Params
](
    result: Result[AValueT, AErrorT]
) -> Callable[
    [Callable[Concatenate[AValueT, Params], Result[BValueT, BErrorT]]],
    Callable[Params, Result[BValueT, BErrorT]],
]:
    def decorator(
        act: Callable[Concatenate[AValueT, Params], Result[BValueT, BErrorT]],
    ) -> Callable[Params, Result[BValueT, BErrorT]]:
        @wraps(act)
        def wrapper(
            *args: Params.args, **kwargs: Params.kwargs
        ) -> Result[BValueT, BErrorT]:
            bresult = result.and_then(lambda value: act(value, *args, **kwargs))
            return cast(Result[BValueT, BErrorT], bresult)

        return wrapper

    return decorator

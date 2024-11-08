from dataclasses import dataclass
from typing import Any, Awaitable, Callable, Concatenate, Self, overload

from result import Err, Ok, Result


def swap[V, E](result: Result[V, E]) -> Result[E, V]:
    match result:
        case Ok(v):
            return Err(v)
        case Err(e):
            return Ok(e)


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


type AnyTuple = tuple[Any, ...]


type ResultList[Values: AnyTuple, Error] = ErrList[Error] | OkList[Values]


@dataclass(frozen=True, slots=True)
class OkList[Values: AnyTuple]:
    __values: Values

    @overload
    def __add__[Error](self, result_list: "ErrList[Error]") -> "ErrList[Error]":
        ...

    @overload
    def __add__[*ValuesTVT, T1](
        self: "OkList[tuple[*ValuesTVT]]", result_list: "OkList[tuple[T1]]"
    ) -> "OkList[tuple[*ValuesTVT, T1]]": ...

    @overload
    def __add__[*ValuesTVT, T1, T2](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "OkList[tuple[T1, T2]]"
    ) -> "OkList[tuple[*ValuesTVT, T1, T2]]": ...

    @overload
    def __add__[*ValuesTVT, T1, T2, T3](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "OkList[tuple[T1, T2, T3]]"
    ) -> "OkList[tuple[*ValuesTVT, T1, T2, T3]]": ...

    @overload
    def __add__[*ValuesTVT, T1, T2, T3, T4](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "OkList[tuple[T1, T2, T3, T4]]"
    ) -> "OkList[tuple[*ValuesTVT, T1, T2, T3, T4]]": ...

    @overload
    def __add__[*ValuesTVT, T1, T2, T3, T4, T5](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "OkList[tuple[T1, T2, T3, T4, T5]]"
    ) -> "OkList[tuple[*ValuesTVT, T1, T2, T3, T4, T5]]": ...

    @overload
    def __add__[*ValuesTVT, T1, T2, T3, T4, T5, T6](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "OkList[tuple[T1, T2, T3, T4, T6]]"
    ) -> "OkList[tuple[*ValuesTVT, T1, T2, T3, T4, T6]]": ...

    @overload
    def __add__[*ValuesTVT, Error, T1](
        self: "OkList[tuple[*ValuesTVT]]",
        result_list: "ResultList[tuple[T1], Error]",
    ) -> "ResultList[tuple[*ValuesTVT, T1], Error]": ...

    def __add__[Error](
        self, result_list: ResultList[AnyTuple, Error]
    ) -> ResultList[AnyTuple, Error]:
        match result_list:
            case OkList(values):
                return OkList(self.__values + values)
            case ErrList(_) as err_list:
                return err_list

    def map[NewValues: AnyTuple](
        self, act: Callable[[Values], NewValues]
    ) -> "OkList[NewValues]":
        return OkList(act(self.__values))

    def map_err(self, _: Any) -> Self:  # noqa: ANN401
        return self


@dataclass(frozen=True, slots=True)
class ErrList[Value]:
    __value: Value

    def __add__(self, _: Any) -> Self:  # noqa: ANN401
        return self

    def map(self, _: Any) -> Self:  # noqa: ANN401
        return self

    def map_err[NewValue](
        self, act: Callable[[Value], NewValue]
    ) -> "ErrList[NewValue]":
        return ErrList(act(self.__value))


@overload
def rlist[Value](result: Ok[Value]) -> OkList[tuple[Value]]: ...

@overload
def rlist[Error](result: Err[Error]) -> ErrList[Error]: ...


def rlist[Value, Error](
    result: Result[Value, Error]
) -> ResultList[tuple[Value], Error]:
    match result:
        case Ok(value):
            return OkList((value, ))
        case Err(error):
            return ErrList(error)


async def sync[ValueT, ErrorT](
    async_result: Result[Awaitable[ValueT], ErrorT],
) -> Result[ValueT, ErrorT]:
    return await async_result.map_async(lambda value: value)

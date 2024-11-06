from dataclasses import dataclass
from functools import partial
from typing import Callable, cast


@dataclass(frozen=True, slots=True)
class Env[ContextT, ValueT]:
    context: ContextT
    value: ValueT


def env[ContextT, ValueT](
    context: ContextT,
) -> Callable[[ValueT], Env[ContextT, ValueT]]:
    act = partial(Env, context)
    return cast(Callable[[ValueT], Env[ContextT, ValueT]], act)


type Just[ValueT] = Env[None, ValueT]


def just[ValueT](value: ValueT) -> Just[ValueT]:
    return Env(None, value)

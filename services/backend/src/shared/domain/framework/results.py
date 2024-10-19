from typing import cast

from result import Err, Ok, Result, is_ok


def swap[V, E](result: Result[V, E]) -> Result[E, V]:
    if is_ok(result):
        return Err(result.ok())

    return Ok(cast(Err[E], result).err())

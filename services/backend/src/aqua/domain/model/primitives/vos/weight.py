from dataclasses import dataclass
from typing import Literal

from result import Err, Ok, Result

from shared.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class Weight(SafeImmutable):
    kilograms: int

    @classmethod
    def with_(cls, *, kilograms: int) -> Result[
        "Weight", Literal["negative_weight_amount"]
    ]:
        if kilograms < 0:
            return Err("negative_weight_amount")

        return Ok(Weight(kilograms=kilograms, is_safe=True))

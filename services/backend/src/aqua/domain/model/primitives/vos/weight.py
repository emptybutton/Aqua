from dataclasses import dataclass

from result import Err, Ok, Result

from shared.domain.framework.safe import SafeImmutable


@dataclass(kw_only=True, frozen=True, slots=True)
class NegativeWeightAmountError: ...


@dataclass(kw_only=True, frozen=True, slots=True)
class Weight(SafeImmutable):
    kilograms: int

    @classmethod
    def with_(cls, *, kilograms: int) -> Result[
        "Weight", NegativeWeightAmountError
    ]:
        if kilograms < 0:
            return Err(NegativeWeightAmountError())

        return Ok(Weight(kilograms=kilograms, is_safe=True))

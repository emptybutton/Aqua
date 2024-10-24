from dataclasses import dataclass

from aqua.domain.model.core.aggregates.user.root import CancellationOutput, User


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryCancellationView:
    user: User
    output: CancellationOutput

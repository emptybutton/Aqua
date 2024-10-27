from dataclasses import dataclass

from aqua.domain.model.core.aggregates.user.root import User


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryRegistrationView:
    user: User

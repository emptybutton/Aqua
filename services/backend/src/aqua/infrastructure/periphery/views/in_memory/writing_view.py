from dataclasses import dataclass

from aqua.domain.model.core.aggregates.user.root import User, WritingOutput


@dataclass(kw_only=True, frozen=True, slots=True)
class InMemoryWritingView:
    user: User
    output: WritingOutput

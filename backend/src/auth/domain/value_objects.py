from dataclasses import dataclass

from src.auth.domain import errors


@dataclass(frozen=True)
class Username:
    text: str

    def __post_init__(self) -> None:
        if len(self.text) <= 0 or len(self.text) > 64:  # noqa: PLR2004
            raise errors.ExtremeUsernameLength()

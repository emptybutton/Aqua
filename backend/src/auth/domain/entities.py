from dataclasses import dataclass, field
from uuid import uuid4, UUID

from auth.domain.value_objects import Username, PasswordHash


@dataclass(kw_only=True)
class User:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    name: Username
    password_hash: PasswordHash

    class AuthorizationError(Error): ...

    class IncorrectPasswordHashForAuthorizationError(AuthorizationError): ...

    def authorize(self, *, password_hash: PasswordHash) -> None:
        if self.password_hash != password_hash:
            raise User.IncorrectPasswordHashForAuthorizationError

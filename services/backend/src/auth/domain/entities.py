from dataclasses import dataclass, field
from enum import Enum, auto
from uuid import UUID, uuid4

from auth.domain.value_objects import (
    PasswordHash,
    SessionLifetime,
    Time,
    Username,
)


@dataclass(kw_only=True)
class PreviousUsername:
    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    username: Username
    change_time: Time | None


@dataclass(kw_only=True)
class User:
    class Error(Exception): ...

    id: UUID = field(default_factory=uuid4)
    name: Username
    password_hash: PasswordHash

    class AuthorizationError(Error): ...

    class IncorrectPasswordHashForAuthorizationError(AuthorizationError): ...

    @dataclass(kw_only=True, frozen=True)
    class AuthorizationOutput:
        current_session: "Session"
        prevous_session: "Session | None" = None
        new_session: "Session | None" = None
        replaced_session: "Session | None" = None
        extended_session: "Session | None" = None

    def authorize(
        self,
        *,
        password_hash: PasswordHash,
        current_time: Time,
        current_session: "Session | None" = None,
    ) -> AuthorizationOutput:
        if self.password_hash != password_hash:
            raise User.IncorrectPasswordHashForAuthorizationError

        result = Session.for_user_with_id(
            self.id,
            current_time=current_time,
            current_session=current_session,
        )

        return User.AuthorizationOutput(
            current_session=result.current_session,
            prevous_session=result.prevous_session,
            new_session=result.new_session,
            replaced_session=result.replaced_session,
            extended_session=result.extended_session,
        )

    def change_name(
        self,
        *,
        new_username: Username,
        current_time: Time,
    ) -> PreviousUsername:
        previous_username = PreviousUsername(
            username=self.name,
            user_id=self.id,
            change_time=current_time,
        )
        self.name = new_username

        return previous_username

    class PasswordChangeError(Error): ...

    class OtherUserSessionForPasswordChangeError(PasswordChangeError): ...

    def change_password(
        self,
        *,
        new_password_hash: PasswordHash,
        other_sessions: tuple["Session", ...],
    ) -> None:
        for other_session in other_sessions:
            if other_session.user_id != self.id:
                raise User.OtherUserSessionForPasswordChangeError

        self.password_hash = new_password_hash

        for other_session in other_sessions:
            other_session.cancel()

    @dataclass(kw_only=True, frozen=True)
    class RegistrationOutput:
        user: "User"
        current_session: "Session"
        prevous_session: "Session | None"

        new_session: "Session | None"
        replaced_session: "Session | None"
        extended_session: "Session | None"

    @classmethod
    def register(
        cls,
        name: Username,
        password_hash: PasswordHash,
        *,
        current_time: Time,
        current_session: "Session | None" = None,
    ) -> RegistrationOutput:
        user = User(name=name, password_hash=password_hash)

        result = Session.for_user_with_id(
            user.id,
            current_time=current_time,
            current_session=current_session,
        )

        return User.RegistrationOutput(
            user=user,
            current_session=result.current_session,
            prevous_session=result.prevous_session,
            new_session=result.new_session,
            replaced_session=result.replaced_session,
            extended_session=result.extended_session,
        )


@dataclass(kw_only=True)
class Session:
    class Error(Exception): ...

    class InactivityReasons(Enum):
        replaced = auto()
        expired = auto()
        cancelled = auto()

    id: UUID = field(default_factory=uuid4)
    user_id: UUID
    lifetime: SessionLifetime
    is_cancelled: bool = False
    next_session_id: UUID | None = None

    @property
    def is_replaced(self) -> bool:
        return self.next_session_id is not None

    def is_expired(self, *, current_time: Time) -> bool:
        return self.lifetime.expired(current_time=current_time)

    def inactivity_reasons_when(
        self, *, current_time: Time
    ) -> frozenset[InactivityReasons]:
        reasons: set[Session.InactivityReasons] = set()

        if self.is_replaced:
            reasons.add(Session.InactivityReasons.replaced)

        if self.is_expired(current_time=current_time):
            reasons.add(Session.InactivityReasons.expired)

        if self.is_cancelled:
            reasons.add(Session.InactivityReasons.cancelled)

        return frozenset(reasons)

    def is_active(self, *, current_time: Time) -> bool:
        return not self.inactivity_reasons_when(current_time=current_time)

    def cancel(self) -> None:
        self.cancelled = True

    def replaced(self, prevous_session: "Session") -> "Session":
        prevous_session.next_session_id = self.id

        return prevous_session

    class AuthenticationError(Error): ...

    class ExpiredForAuthenticationError(AuthenticationError): ...

    class CancelledForAuthenticationError(AuthenticationError): ...

    class ReplacedForAuthenticationError(AuthenticationError): ...

    def authenticate(self, *, current_time: Time) -> "Session":
        reasons = self.inactivity_reasons_when(current_time=current_time)

        if Session.InactivityReasons.replaced in reasons:
            raise Session.ReplacedForAuthenticationError

        if Session.InactivityReasons.expired in reasons:
            raise Session.ExpiredForAuthenticationError

        if Session.InactivityReasons.cancelled in reasons:
            raise Session.CancelledForAuthenticationError

        return self.extend(current_time=current_time)

    def extend(self, *, current_time: Time) -> "Session":
        self.lifetime = self.lifetime.extend(current_time=current_time)
        return self

    @dataclass(kw_only=True, frozen=True)
    class CreationForUserOutput:
        current_session: "Session"
        prevous_session: "Session | None" = None

        new_session: "Session | None" = None
        replaced_session: "Session | None" = None
        extended_session: "Session | None" = None

    @classmethod
    def for_user_with_id(
        cls,
        user_id: UUID,
        *,
        current_time: Time,
        current_session: "Session | None" = None,
    ) -> CreationForUserOutput:
        if current_session is not None and not current_session.is_active(
            current_time=current_time
        ):
            current_session = None

        if current_session is not None and current_session.user_id == user_id:
            current_session = current_session.extend(current_time=current_time)

            return Session.CreationForUserOutput(
                current_session=current_session,
                extended_session=current_session,
            )

        prevous_session = current_session

        lifetime = SessionLifetime(start_time=current_time)
        current_session = Session(user_id=user_id, lifetime=lifetime)

        if prevous_session is not None:
            prevous_session = current_session.replaced(prevous_session)

        return Session.CreationForUserOutput(
            current_session=current_session,
            prevous_session=prevous_session,
            new_session=current_session,
            replaced_session=prevous_session,
        )

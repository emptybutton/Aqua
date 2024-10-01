from dataclasses import dataclass
from typing import Literal, TypeAlias
from uuid import UUID, uuid4

from auth.domain.models.auth.aggregates.account.internal import (
    account_name as _account_name,
)
from auth.domain.models.auth.aggregates.account.internal import (
    session as _session,
)
from auth.domain.models.auth.pure.vos import password as _password
from auth.domain.models.auth.pure.vos import time as _time
from shared.domain.pure import entity as _entity
from shared.domain.pure.ports.effect import Effect


@dataclass(kw_only=True, frozen=True, slots=True)
class NameChange(_entity.MutationEvent[UUID]):
    new_name_text: str


AccountEvent: TypeAlias = (
    NameChange
)


@dataclass(kw_only=True, eq=False)
class Account(_entity.Entity[UUID, AccountEvent]):
    class Error(Exception): ...

    id: UUID
    current_name: _account_name.AccountName
    prevous_names: set[_account_name.AccountName]
    sessions: set[_session.Session]
    password_hash: _password.PasswordHash

    def session_with(self, session_id: UUID) -> _session.Session | None:
        for session in self.sessions:
            if session.id == session_id:
                return session

        return None

    class AuthenticationError(Error): ...

    class NoSessionError(AuthenticationError): ...

    class ExpiredForAuthenticationError(AuthenticationError): ...

    class CancelledForAuthenticationError(AuthenticationError): ...

    class ReplacedForAuthenticationError(AuthenticationError): ...

    def authenticate(
        self, *, session_id: UUID, current_time: _time.Time, effect: Effect,
    ) -> _session.Session:
        session = self.session_with(session_id)

        if not session:
            raise Account.NoSessionError

        reasons = session.inactivity_reasons_when(current_time=current_time)

        if "replaced" in reasons:
            raise Account.ReplacedForAuthenticationError

        if "expired" in reasons:
            raise Account.ExpiredForAuthenticationError

        if "cancelled" in reasons:
            raise Account.CancelledForAuthenticationError

        _session.extend(session, current_time=current_time, effect=effect)


    def change_name(
        self,
        *,
        new_name_text: str,
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


class LoginError(Exception): ...


class IncorrectPasswordHashForLoginError(LoginError): ...


def login_to(
    account: Account,
    *,
    password_hash: _password.PasswordHash,
    current_time: _time.Time,
    current_session: _session.Session | None = None,
    effect: Effect,
) -> None:
    if account.password_hash != password_hash:
        raise IncorrectPasswordHashForLoginError

    return _session.issue_session(
        account_id=account.id,
        current_time=current_time,
        current_session=current_session,
        effect=effect,
    )

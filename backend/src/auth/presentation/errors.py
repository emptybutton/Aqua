from typing import TypeAlias

from src.auth.domain import errors


ValidationError: TypeAlias = errors.DomainError

ExtremeUsernameLength: TypeAlias = errors.ExtremeUsernameLength

WeekPassword: TypeAlias = errors.WeekPassword

TooLongPassword: TypeAlias = errors.TooLongPassword

ExtremePasswordHashLength: TypeAlias = errors.ExtremePasswordHashLength

NotUTCExpirationDate: TypeAlias = errors.NotUTCExpirationDate

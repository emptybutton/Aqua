from typing import TypeAlias

from src.auth.domain import errors


ValidationError: TypeAlias = errors.DomainError

EmptyUsername: TypeAlias = errors.EmptyUsername

WeekPassword: TypeAlias = errors.WeekPassword

EmptyPasswordHash: TypeAlias = errors.EmptyPasswordHash

NotUTCExpirationDate: TypeAlias = errors.NotUTCExpirationDate

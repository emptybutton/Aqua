from typing import TypeAlias

from aqua.domain import errors


ValidationError: TypeAlias = errors.DomainError

IncorrectWaterAmount: TypeAlias = errors.IncorrectWaterAmount

IncorrectWeightAmount: TypeAlias = errors.IncorrectWeightAmount

NoWeightForWaterBalance: TypeAlias = errors.NoWeightForWaterBalance

ExtremeWeightForWaterBalance: TypeAlias = errors.ExtremeWeightForWaterBalance

NotUTCRecordingTime: TypeAlias = errors.NotUTCRecordingTime

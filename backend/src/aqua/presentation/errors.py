from typing import TypeAlias

from src.aqua.domain import errors


ValidationError: TypeAlias = errors.DomainError

NoWater: TypeAlias = errors.NoWater

NoWeight: TypeAlias = errors.NoWeight

NoWeightForWaterBalance: TypeAlias = errors.NoWeightForWaterBalance

ExtremeWeightForWaterBalance: TypeAlias = errors.ExtremeWeightForWaterBalance

NotUTCRecordingTime: TypeAlias = errors.NotUTCRecordingTime

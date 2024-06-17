class DomainError(Exception): ...


class IncorrectWaterAmount(DomainError): ...


class IncorrectWeightAmount(DomainError): ...


class NoWeightForWaterBalance(DomainError): ...


class ExtremeWeightForWaterBalance(DomainError): ...


class NotUTCRecordingTime(DomainError): ...

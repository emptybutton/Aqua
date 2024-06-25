export class ValidationError extends Error {}

export class EmptyUsernameError extends ValidationError {}

export class NegativeWaterAmountError extends ValidationError {}

export class FloatWaterAmountError extends ValidationError {}

export class NegativeWeightAmountError extends ValidationError {}

export class FloatWeightAmountError extends ValidationError {}

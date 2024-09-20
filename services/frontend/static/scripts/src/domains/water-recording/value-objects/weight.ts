import { VOError } from "../../shared/value-objects/error.js";

export class WeightError extends VOError {}

export class InvalidityReasonsForWeightError extends WeightError {}

export class Weight {
    constructor(readonly kilograms: number) {
        if (new Set(invalidityReasonsFor(kilograms)).size !== 0)
            throw new InvalidityReasonsForWeightError();
    }
}

export class WeightForTargetError extends WeightError {}

export class InvalidAmountWeightForTargetError extends WeightForTargetError {}

export class WeightForTarget extends Weight {
    constructor(kilograms: number) {
        super(kilograms);
        
        if (this.kilograms < 30 || this.kilograms > 150)
            throw new InvalidAmountWeightForTargetError();
    }
}

export enum InvalidityReasons { negativeAmount, floatAmount, nanAmount }

export function *invalidityReasonsFor(kilograms: number): Generator<InvalidityReasons, void, void> {
    if (isNaN(kilograms)) {
        yield InvalidityReasons.nanAmount;
        return;
    }

    if (kilograms < 0)
        yield InvalidityReasons.negativeAmount;

    if (!Number.isInteger(kilograms))
        yield InvalidityReasons.floatAmount;
}

export class InvalidWeightError extends WeightError {}

export class NoReasonsForInvalidWeightError extends InvalidWeightError {}

export class InvalidWeight {
    constructor(
        readonly kilograms: number,
        readonly reasons: Set<InvalidityReasons>,
    ) {
        Object.freeze(this.reasons);

        if (this.reasons.size === 0)
            throw new NoReasonsForInvalidWeightError();
    }

    static with(kilograms: number): InvalidWeight {
        let reasons = new Set(invalidityReasonsFor(kilograms));

        return new InvalidWeight(kilograms, reasons);
    }
}

export type AnyWeight = Weight | InvalidWeight;

export function anyWith(kilograms: number): AnyWeight {
    try {
        return new WeightForTarget(kilograms);
    }
    catch (error) {
        if (error instanceof InvalidityReasonsForWeightError)
            return InvalidWeight.with(kilograms);

        if (error instanceof InvalidAmountWeightForTargetError)
            return new Weight(kilograms);

        throw error;
    }
}

export function isInvalid(weight: AnyWeight): weight is InvalidWeight {
    return weight instanceof InvalidWeight;
}

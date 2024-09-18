import { VOError } from "../../shared/value-objects/error.js";

export class WeightError extends VOError {}

export class InvalidityReasonsForWeightError extends WeightError {}

export class Weight {
    constructor(readonly kilograms: number) {
        if (invalidityReasonsFor(kilograms).next().value === undefined)
            throw new InvalidityReasonsForWeightError();
    }
}

export enum InvalidityReasons { negativeAmount, floatAmount }

export function *invalidityReasonsFor(kilograms: number): Generator<InvalidityReasons, void, void> {
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
}

export type AnyWeight = Weight | InvalidWeight;

export function anyWith(kilograms: number): AnyWeight {
    let reasons = new Set(invalidityReasonsFor(kilograms));

    if (reasons.size !== 0)
        return new InvalidWeight(kilograms, reasons);

    return new Weight(kilograms);
}

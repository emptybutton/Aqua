import { VOError } from "../../shared/value-objects/error.js";

export class WeightError extends VOError {}

export class NegativeAmountError extends WeightError {}

export class FloatAmountError extends WeightError {}

export class Weight {
    constructor(readonly kilograms: number) {
        if (kilograms < 0)
            throw new NegativeAmountError();

        if (!Number.isInteger(kilograms))
            throw new FloatAmountError();
    }
}

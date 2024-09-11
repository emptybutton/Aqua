import { VOError } from "../../shared/value-objects/error.js";

export class WaterError extends VOError {}

export class NegativeAmountError extends WaterError {}

export class FloatAmountError extends WaterError {}

export class Water {
    constructor(readonly milliliters: number) {
        if (milliliters < 0)
            throw new NegativeAmountError();

        if (!Number.isInteger(milliliters))
            throw new FloatAmountError();
    }
}

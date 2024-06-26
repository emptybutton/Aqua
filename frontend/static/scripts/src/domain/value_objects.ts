import {
    EmptyUsernameError,
    NegativeWaterAmountError,
    FloatWaterAmountError,
    NegativeWeightAmountError,
    FloatWeightAmountError,
} from "./errors.js";

export type UUID = string;

export class Username {
    constructor(readonly text: string) {
        if (text === "")
            throw new EmptyUsernameError();
    }
}

export type JWT = string;

export abstract class PasswordPower {}

export class StrongPasswordPower extends PasswordPower {}

export class WeakPasswordPower extends PasswordPower {
    constructor(readonly reasons: Set<WeakPasswordReasons>) {
        super();
    }
}

export enum WeakPasswordReasons {
    tooShort,
    onlySmallLetters,
    onlyСapitalLetters,
    onlyDigits,
    noDigits, 
}

export class Password<PowerT extends PasswordPower = PasswordPower> {
    private constructor(readonly text: string, readonly power: PowerT) {}

    static with(text: string): Password {
        const weaknessReasons = new Set(Password._weaknessReasonsFor(text));
        let power;

        if (weaknessReasons.size === 0)
            power = new StrongPasswordPower();
        else
            power = new WeakPasswordPower(weaknessReasons);

        return new Password(text, power);
    }

    private static *_weaknessReasonsFor(text: string) {
        if (text.length < 8)
            yield WeakPasswordReasons.tooShort;

        if (text.toLocaleLowerCase() === text)
            yield WeakPasswordReasons.onlySmallLetters;

        if (text.toLocaleUpperCase() === text)
            yield WeakPasswordReasons.onlyСapitalLetters;

        if (Password._hasOnlyDigits(text))
            yield WeakPasswordReasons.onlyDigits;

        if (Password._hasNoDigits(text))
            yield WeakPasswordReasons.noDigits;
    }

    private static _hasOnlyDigits(text: string): boolean {
        return !isNaN(parseInt(text));
    }

    private static _hasNoDigits(text: string): boolean {
        return !text.split('').some(char => char >= '0' && char <= '9');
    }
}

export type StrongPassword = Password<StrongPasswordPower>

export type WeakPassword = Password<WeakPasswordPower>

export class Water {
    constructor(readonly milliliters: number) {
        if (milliliters < 0)
            throw new NegativeWaterAmountError();

        if (!Number.isInteger(milliliters))
            throw new FloatWaterAmountError();
    }
}

export class WaterBalance {
    constructor(readonly water: Water) {}
}

export class Glass {
    constructor(readonly capacity: Water) {}
}

export class Weight {
    constructor(readonly kilograms: number) {
        if (kilograms < 0)
            throw new NegativeWeightAmountError();

        if (!Number.isInteger(kilograms))
            throw new FloatWeightAmountError();
    }
}

export enum WaterBalanceStatus {
    good = 1,
    not_enough_water = 2,
    excess_water = 3,
}

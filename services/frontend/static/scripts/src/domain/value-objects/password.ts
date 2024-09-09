export abstract class Power {}

export class StrongPower extends Power {}

export class WeakPower extends Power {
    constructor(readonly reasons: Set<WeaknessReasons>) {
        super();
    }
}

export enum WeaknessReasons {
    tooShort,
    onlySmallLetters,
    onlyCapitalLetters,
    onlyDigits,
    noDigits, 
}

export class Password<PowerT extends Power = Power> {
    private constructor(readonly text: string, readonly power: PowerT) {}

    static with(text: string): Password {
        const weaknessReasons = new Set(_weaknessReasonsFor(text));
        let power;

        if (weaknessReasons.size === 0)
            power = new StrongPower();
        else
            power = new WeakPower(weaknessReasons);

        return new Password(text, power);
    }
}

export type StrongPassword = Password<StrongPower>

export type WeakPassword = Password<WeakPower>

function *_weaknessReasonsFor(text: string) {
    if (text.length < 8)
        yield WeaknessReasons.tooShort;

    if (text.toLocaleLowerCase() === text)
        yield WeaknessReasons.onlySmallLetters;

    if (text.toLocaleUpperCase() === text)
        yield WeaknessReasons.onlyCapitalLetters;

    if (_hasOnlyDigits(text))
        yield WeaknessReasons.onlyDigits;

    if (_hasNoDigits(text))
        yield WeaknessReasons.noDigits;
}

function _hasOnlyDigits(text: string): boolean {
    return !isNaN(parseInt(text));
}

function _hasNoDigits(text: string): boolean {
    return !text.split('').some(char => char >= '0' && char <= '9');
}

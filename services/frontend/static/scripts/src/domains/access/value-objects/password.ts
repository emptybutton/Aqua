export abstract class Power {}

export class StrongPower extends Power {}

export class WeakPower extends Power {
    constructor(readonly reasons: Set<WeaknessReasons>) {
        super();
        Object.freeze(this.reasons);
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
    static with(text: string): Password {
        const weaknessReasons = new Set(_weaknessReasonsFor(text));
        let power;

        if (weaknessReasons.size === 0)
            power = new StrongPower();
        else
            power = new WeakPower(weaknessReasons);

        return new Password(text, power);
    }

    get isWeak(): boolean {
        return this.power instanceof WeakPower;
    }

    private constructor(readonly text: string, readonly power: PowerT) {}
}

export type StrongPassword = Password<StrongPower>

export type WeakPassword = Password<WeakPower>

function *_weaknessReasonsFor(text: string) {
    if (text.length < 8)
        yield WeaknessReasons.tooShort;

    if (text.length !== 0) {
        if (text.toLocaleLowerCase() === text)
            yield WeaknessReasons.onlySmallLetters;

        if (text.toLocaleUpperCase() === text)
            yield WeaknessReasons.onlyCapitalLetters;
    }

    if (_hasNoDigits(text))
        yield WeaknessReasons.noDigits;

    else if (_hasOnlyDigits(text))
        yield WeaknessReasons.onlyDigits;
}

function _hasOnlyDigits(text: string): boolean {
    return _digitAmountIn(text) === text.length;
}

function _hasNoDigits(text: string): boolean {
    return _digitAmountIn(text) === 0;
}

function _digitAmountIn(text: string): number {
    let amount = 0;
    let digits = new Set(['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']);

    for (const char of text) {
        if (digits.has(char))
            amount++;
    }

    return amount; 
}

import { VOError } from "../../shared/value-objects/error.js";
import { maybe } from "../../shared/value-objects/maybe.js";

export class UsernameError extends VOError {}

export class EmptyError extends UsernameError {}

export class Username {
    constructor(readonly text: string) {
        if (text === "")
            throw new EmptyError();
    }
}

export class InvalidUsername {
    constructor(readonly text: string) {}
}

export type AnyUsername = Username | InvalidUsername;

export function anyWith(text: string): AnyUsername {
    let username = maybe(() => new Username(text));

    return username === undefined ? new InvalidUsername(text) : username
}

import { Password, Username } from "../domain/value_objects.js";
import * as gateway from "../infrastructure/gateway.js";
import { jwtStorage } from "../infrastructure/storages.js";

export async function authorize(
    username: Username,
    password: Password,
): Promise<boolean> {
    const result = await gateway.authorize(username, password);

    if (result === undefined)
        return false;

    jwtStorage.jwt = result.jwt;

    return true;
}

export function logout(): void {
    jwtStorage.jwt = null;
}

export function authorizationCompleted(): boolean {
    return jwtStorage.jwt !== null;
}

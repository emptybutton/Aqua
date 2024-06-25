import { Password, Username } from "../domain/value_objects";
import * as gateway from "../facades/gateway";
import { jwtStorage } from "../facades/storages";

export async function authorize(
    username: Username,
    password: Password,
): Promise<boolean> {
    const result = await gateway.authorize(username, password);

    if (result === undefined)
        return false;

    jwtStorage.set(result.jwt);

    return true;
}

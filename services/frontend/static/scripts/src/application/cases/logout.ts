import * as storages from "../ports/storages.js";

export async function perform(jwtStorage: storages.JWTStorage): Promise<void> {
    jwtStorage.jwt = undefined;
}

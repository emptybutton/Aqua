import { JWT } from "../../domain/value_objects.js";

export interface JWTStorage {
    get jwt(): JWT | undefined,
    set jwt(newJwt: JWT | undefined),
}

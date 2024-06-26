import { JWT } from "../domain/value_objects.js";

export const jwtStorage = {
    set jwt(jwt: JWT | null) {
        if (jwt === null)
            localStorage.removeItem("jwt");
        else
            localStorage.setItem("jwt", jwt);
    },

    get jwt(): JWT | null {
        return localStorage.getItem("jwt");
    },
}

import { JWT } from "../domain/value_objects";

export const jwtStorage = {
    set(jwt: JWT): void {
        localStorage.setItem("jwt", jwt);
    },

    get(): JWT | null {
        return localStorage.getItem("jwt");
    },
}

import * as storages from "../../application/ports/storages.js";
import * as vos from "../../domain/value_objects.js";

export const localJwtStorage: storages.JWTStorage = {
    set jwt(jwt: vos.JWT | undefined) {
        if (jwt === undefined)
            localStorage.removeItem("jwt");
        else
            localStorage.setItem("jwt", jwt.text);
    },

    get jwt(): vos.JWT | undefined {
        let jwtText = localStorage.getItem("jwt");
        return jwtText === null ? undefined : new vos.JWT(jwtText);
    },
}

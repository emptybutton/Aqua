import * as views from "../ports/views.js";
import * as storages from "../ports/storages.js";

export async function perform(
    windowView: views.WindowView,
    jwtStorage: storages.JWTStorage,
): Promise<void> {
    if (jwtStorage.jwt === undefined)
        windowView.redrawForAuthorization();
}

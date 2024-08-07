import { adapterContainer } from "../containers.js";
import * as authenticate from "../../../application/cases/authenticate.js";

export async function perform(): Promise<void> {
    await authenticate.perform(
        adapterContainer.getWindowView(),
        adapterContainer.getJWTStorage(),
    );
}

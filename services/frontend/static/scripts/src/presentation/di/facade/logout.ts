import { adapterContainer } from "../containers.js";
import * as logout from "../../../application/cases/logout.js";

export async function perform(
): Promise<void> {
    await logout.perform(adapterContainer.getJWTStorage());
}

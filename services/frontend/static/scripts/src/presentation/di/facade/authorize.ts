import { adapterContainer } from "../containers.js";
import * as authorize from "../../../application/cases/authorize.js";

export async function perform(
    username: string,
    password: string,
    usernameFieldElement: HTMLElement,
    passwordFieldElement: HTMLElement,
): Promise<void> {
    await authorize.perform(
        username,
        password,
        adapterContainer.getBackendGateway(),
        adapterContainer.getLogger(),
        adapterContainer.getFormFieldView(usernameFieldElement),
        adapterContainer.getFormFieldView(passwordFieldElement),
        adapterContainer.getUsernamesOfUnregisteredUsers(),
        adapterContainer.getJWTStorage(),
    );
}

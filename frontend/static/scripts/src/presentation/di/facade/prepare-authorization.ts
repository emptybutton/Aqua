import { adapterContainer } from "../containers.js";
import * as prepareAuthorization from "../../../application/cases/prepare-authorization.js";

export async function perform(
    username: string,
    password: string,
    usernameFieldElement: HTMLElement,
    passwordFieldElement: HTMLElement,
): Promise<void> {
    await prepareAuthorization.perform(
        username,
        password,
        adapterContainer.getFormFieldView(usernameFieldElement),
        adapterContainer.getFormFieldView(passwordFieldElement),
        adapterContainer.getUsernamesOfUnregisteredUsers(),
    );
}

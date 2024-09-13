import { adapterContainer } from "../containers.js";
import * as _login from "../../../application/cases/login.js";

export async function login(
    username: string,
    password: string,
    usernameFieldElement: HTMLElement,
    passwordFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _login.login(
        username,
        password,
        adapterContainer.backend,
        adapterContainer.logger,
        adapterContainer.formFieldViewOf(usernameFieldElement),
        adapterContainer.formFieldViewOf(passwordFieldElement),
        adapterContainer.usernamesOfUnregisteredUsers,
        adapterContainer._invalidCredentialSet,
        adapterContainer.windowView,
        adapterContainer.loginNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    );
}

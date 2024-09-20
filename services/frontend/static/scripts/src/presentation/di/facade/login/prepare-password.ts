import { adapterContainer } from "../../containers.js";
import * as _prepare from "../../../../application/usecases/login/prepare.js";

export async function execute(
    username: string,
    password: string,
    usernameFieldElement: HTMLElement,
    passwordFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _prepare.execute(
        username,
        password,
        _prepare.Priority.forPassword,
        adapterContainer.formFieldViewOf(usernameFieldElement),
        adapterContainer.formFieldViewOf(passwordFieldElement),
        adapterContainer.usernamesOfUnregisteredUsers,
        adapterContainer.invalidCredentialSet,
        adapterContainer.loginNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    );
}

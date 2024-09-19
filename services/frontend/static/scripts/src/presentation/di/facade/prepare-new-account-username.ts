import { adapterContainer } from "../containers.js";
import * as _prepareNewAccountUsername from "../../../application/cases/prepare-new-account-username.js";

export async function prepareNewAccountUsername(
    username: string,
    usernameFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    _prepareNewAccountUsername.prepareNewAccountUsername(
        username,
        adapterContainer.formFieldViewOf(usernameFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
        adapterContainer.usernamesOfRegisteredUsers,
        adapterContainer.usernamesOfUnregisteredUsers,
        adapterContainer.timeoutForUsernameAvailability,
        adapterContainer.backend,
        adapterContainer.logger,
    );
}

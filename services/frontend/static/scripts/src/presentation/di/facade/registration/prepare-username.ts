import { adapterContainer } from "../../containers.js";
import * as _prepareUsername from "../../../../application/usecases/registration/prepare-username.js";

export async function execute(
    username: string,
    usernameFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    _prepareUsername.execute(
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

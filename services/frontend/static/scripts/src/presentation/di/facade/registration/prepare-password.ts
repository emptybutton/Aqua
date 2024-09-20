import { adapterContainer } from "../../containers.js";
import * as _preparePassword from "../../../../application/usecases/registration/prepare-password.js";

export async function execute(
    password: string,
    passwordFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    _preparePassword.execute(
        password,
        adapterContainer.formFieldViewOf(passwordFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    )
}

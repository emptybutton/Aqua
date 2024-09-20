import { adapterContainer } from "../containers.js";
import * as _prepareNewAccountPassword from "../../../application/cases/prepare-new-account-password.js";

export async function prepareNewAccountPassword(
    password: string,
    passwordFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    _prepareNewAccountPassword.prepareNewAccountPassword(
        password,
        adapterContainer.formFieldViewOf(passwordFieldElement),
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    )
}

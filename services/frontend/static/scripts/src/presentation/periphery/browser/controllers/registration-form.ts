import * as _prepareUsername from "../../../di/facade/registration/prepare-username.js";
import * as _preparePassword from "../../../di/facade/registration/prepare-password.js";
import * as _closeNotification from "../../../di/facade/registration/close-notification.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
    // pushButtonElement: HTMLElement,
): void {
    const handleUsername = async () => await _prepareUsername.execute(
        usernameElement.value,
        usernameElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handlePassword = async () => await _preparePassword.execute(
        passwordElement.value,
        passwordElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleNotificationCloseButtonActivation = async () => {
        await _closeNotification.execute(
            notificationSignalElement,
            notificationTextElement,
        )
    };

    usernameElement.addEventListener("input", handleUsername);
    usernameElement.addEventListener("focus", handleUsername);
    passwordElement.addEventListener("input", handlePassword);
    passwordElement.addEventListener("focus", handlePassword);
    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );
}

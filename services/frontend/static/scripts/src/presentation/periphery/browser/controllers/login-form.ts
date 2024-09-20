import * as _login from "../../../di/facade/login/login.js";
import * as _prepareUsername from "../../../di/facade/login/prepare-username.js";
import * as _preparePassword from "../../../di/facade/login/prepare-password.js";
import * as _closeNotification from "../../../di/facade/login/close-notification.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
    pushButtonElement: HTMLElement,
): void {
    const handleUsernameInput = async () => await _prepareUsername.execute(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
        passwordElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handlePasswordInput = async () => await _preparePassword.execute(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
        passwordElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handlePushButtonActivation = async () => await _login.execute(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
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

    usernameElement.addEventListener("input", handleUsernameInput);
    passwordElement.addEventListener("input", handlePasswordInput);
    pushButtonElement.addEventListener("click", handlePushButtonActivation);
    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );
}

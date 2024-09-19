import * as _login from "../../../di/facade/login.js";
import * as _prepareNewAccountUsername from "../../../di/facade/prepare-new-account-username.js";
import * as _closeNewAccountNotification from "../../../di/facade/close-new-account-notification.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
    // pushButtonElement: HTMLElement,
): void {
    const handleUsername = async () => await _prepareNewAccountUsername.prepareNewAccountUsername(
        usernameElement.value,
        usernameElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleNotificationCloseButtonActivation = async () => {
        await _closeNewAccountNotification.closeNewAccountNotification(
            notificationSignalElement,
            notificationTextElement,
        )
    };

    usernameElement.addEventListener("input", handleUsername);
    usernameElement.addEventListener("focus", handleUsername);
    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );
}

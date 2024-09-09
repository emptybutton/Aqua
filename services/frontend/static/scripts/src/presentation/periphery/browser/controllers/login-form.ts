import * as _login from "../../../di/facade/login.js";
import * as _prepareToLogin from "../../../di/facade/prepare-to-login.js";
import * as _closeLoginNotification from "../../../di/facade/close-login-notification.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    notificationElement: HTMLElement,
    pushButtonElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
): void {
    const handleDataInput = async (priority: _prepareToLogin.Priority) => {
        await _prepareToLogin.prepareToLogin(
            usernameElement.value,
            passwordElement.value,
            priority,
            usernameElement,
            passwordElement,
            notificationElement,
        );
    }
    const handleUsernameInput = async () => await handleDataInput(
        _prepareToLogin.Priority.forUsername,
    );
    const handlePasswordInput = async () => await handleDataInput(
        _prepareToLogin.Priority.forPassword,
    );

    const handlePushButtonActivation = async () => await _login.login(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
        passwordElement,
        notificationElement,
    );

    const handleNotificationCloseButtonActivation = async () => {
        await _closeLoginNotification.closeLoginNotification(
            notificationElement,
        )
    };

    usernameElement.addEventListener("input", handleUsernameInput);
    passwordElement.addEventListener("input", handlePasswordInput);
    pushButtonElement.addEventListener("click", handlePushButtonActivation);
    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );
}

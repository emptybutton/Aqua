import * as _prepareUsername from "../../../../di/facade/registration/prepare-username.js";
import * as _preparePassword from "../../../../di/facade/registration/prepare-password.js";
import * as _prepareWeight from "../../../../di/facade/registration/prepare-weight.js";
import * as _closeNotification from "../../../../di/facade/registration/close-notification.js";
import { parseOptional } from "../parsers.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    weightElement: HTMLInputElement | HTMLTextAreaElement,
    targetWaterBalanceElement: HTMLInputElement | HTMLTextAreaElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
    // pushButtonElement: HTMLElement,
): void {
    const handleUsername = () => _prepareUsername.execute(
        usernameElement.value,
        usernameElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handlePassword = () => _preparePassword.execute(
        passwordElement.value,
        passwordElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleWeight = () => _prepareWeight.execute(
        parseOptional(weightElement.value),
        parseOptional(targetWaterBalanceElement.value),
        weightElement,
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

    weightElement.addEventListener("input", handleWeight);
    weightElement.addEventListener("focus", handleWeight);

    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );
}

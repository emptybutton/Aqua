import * as _prepareUsername from "../../../../di/facade/registration/prepare-username.js";
import * as _preparePassword from "../../../../di/facade/registration/prepare-password.js";
import * as _prepareWeight from "../../../../di/facade/registration/prepare-weight.js";
import * as _prepareTarget from "../../../../di/facade/registration/prepare-target.js";
import * as _prepareGlass from "../../../../di/facade/registration/prepare-glass.js";
import * as _closeNotification from "../../../../di/facade/registration/close-notification.js";
import * as _createAccount from "../../../../di/facade/registration/create-account.js";
import { parseOptional } from "../parsers.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    weightElement: HTMLInputElement | HTMLTextAreaElement,
    targetWaterBalanceElement: HTMLInputElement | HTMLTextAreaElement,
    glassElement: HTMLInputElement | HTMLTextAreaElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    notificationCloseButtonElement: HTMLElement,
    pushButtonElement: HTMLElement,
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
        targetWaterBalanceElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleTarget = () => _prepareTarget.execute(
        parseOptional(targetWaterBalanceElement.value),
        parseOptional(weightElement.value),
        targetWaterBalanceElement,
        weightElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleGlass = () => _prepareGlass.execute(
        parseOptional(glassElement.value),
        glassElement,
        notificationSignalElement,
        notificationTextElement,
    );

    const handleNotificationCloseButtonActivation = async () => {
        await _closeNotification.execute(
            notificationSignalElement,
            notificationTextElement,
        )
    };

    const handlePushButtonActivation = () => _createAccount.execute(
        usernameElement.value,
        passwordElement.value,
        parseOptional(weightElement.value),
        parseOptional(targetWaterBalanceElement.value),
        parseOptional(glassElement.value),
        notificationSignalElement,
        notificationTextElement,
        usernameElement,
        pushButtonElement,
    );

    usernameElement.addEventListener("input", handleUsername);
    usernameElement.addEventListener("focus", handleUsername);

    passwordElement.addEventListener("input", handlePassword);
    passwordElement.addEventListener("focus", handlePassword);

    weightElement.addEventListener("input", handleWeight);
    weightElement.addEventListener("focus", handleWeight);

    targetWaterBalanceElement.addEventListener("input", handleTarget);
    targetWaterBalanceElement.addEventListener("focus", handleTarget);

    glassElement.addEventListener("input", handleGlass);
    glassElement.addEventListener("focus", handleGlass);

    notificationCloseButtonElement.addEventListener(
        "click", handleNotificationCloseButtonActivation
    );

    pushButtonElement.addEventListener("click", handlePushButtonActivation);
}

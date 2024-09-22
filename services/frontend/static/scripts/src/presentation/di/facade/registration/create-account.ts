import { adapterContainer } from "../../containers.js";
import * as _createAccount from "../../../../application/usecases/registration/create-account.js";

export async function execute(
    usernameText: string,
    passwordText: string,
    weightKilograms: number | undefined,
    targetWaterBalanceMilliliters: number | undefined,
    glassCapacityMilliliters: number | undefined,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
    usernameFieldElement: HTMLElement,
    activationButtonElement: HTMLElement
): Promise<void> {
    await _createAccount.execute(
        usernameText,
        passwordText,
        weightKilograms,
        targetWaterBalanceMilliliters,
        glassCapacityMilliliters,
        adapterContainer.registrationNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
        adapterContainer.formFieldViewOf(usernameFieldElement),
        adapterContainer.windowView,
        adapterContainer.buttonTernaryViewOf(activationButtonElement),
        adapterContainer.registrationButtonTimeout,
        adapterContainer.redirectionTimeout,
        adapterContainer.usernamesOfRegisteredUsers,
        adapterContainer.backend,
        adapterContainer.logger,
    );
}

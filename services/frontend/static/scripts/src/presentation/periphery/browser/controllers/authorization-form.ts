import * as authorize from "../../../di/facade/authorize.js";
import * as prepareAuthorization from "../../../di/facade/prepare-authorization.js";

export function constructControllers(
    usernameElement: HTMLInputElement | HTMLTextAreaElement,
    passwordElement: HTMLInputElement | HTMLTextAreaElement,
    buttonElement: HTMLElement,
): void {
    const handleDataInput = async () => await prepareAuthorization.perform(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
        passwordElement,
    )

    const handleButtonActivation = async () => await authorize.perform(
        usernameElement.value,
        passwordElement.value,
        usernameElement,
        passwordElement,
    )

    usernameElement.addEventListener("input", handleDataInput);
    passwordElement.addEventListener("input", handleDataInput);
    buttonElement.addEventListener("click", handleButtonActivation);
}

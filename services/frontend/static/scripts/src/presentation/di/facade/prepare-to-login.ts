import { adapterContainer } from "../containers.js";
import * as _prepareToLogin from "../../../application/cases/prepare-to-login.js";

export enum Priority { forUsername, forPassword }

export async function prepareToLogin(
    username: string,
    password: string,
    priority: Priority,
    usernameFieldElement: HTMLElement,
    passwordFieldElement: HTMLElement,
    notificationSignalElement: HTMLElement,
    notificationTextElement: HTMLElement,
): Promise<void> {
    await _prepareToLogin.prepareToLogin(
        username,
        password,
        _facadePriorityOf(priority),
        adapterContainer.formFieldViewOf(usernameFieldElement),
        adapterContainer.formFieldViewOf(passwordFieldElement),
        adapterContainer.usernamesOfUnregisteredUsers,
        adapterContainer.invalidCredentialSet,
        adapterContainer.loginNotificationViewOf(
            notificationSignalElement,
            notificationTextElement,
        ),
    );
}

function _facadePriorityOf(priority: _prepareToLogin.Priority): Priority {
    if (priority === _prepareToLogin.Priority.forUsername)
        return Priority.forUsername;
    else if (priority === _prepareToLogin.Priority.forPassword)
        return Priority.forPassword;
    else
        throw new Error("ivalid priority")
}

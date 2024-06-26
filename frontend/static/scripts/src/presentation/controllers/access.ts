import { Password, StrongPasswordPower, Username } from "../../domain/value_objects.js";
import { authorize, logout } from "../../services/access.js";
import { FormView, FormFieldView, redrawByValidation } from "../views/forms.js";
import { ContainingElement } from "../views/variations.js";
import * as locations from "../views/locations.js";
import * as text from "../views/text.js";

export function constructAuthorizationFormControllers(
    formView: FormView,
    usernameView: FormFieldView<ContainingElement>,
    passwordView: FormFieldView<ContainingElement>,
    buttonElement: HTMLElement,
): void {
    const handleUsernameView = () => redrawByValidation(
        usernameView,
        () => new Username(usernameView.element.value),
    );

    const handlePasswordView = () => {
        const password = Password.with(passwordView.element.value);

        if (password.power instanceof StrongPasswordPower) {
            passwordView.redrawValid();
            return password;
        }
        else
            passwordView.redrawInvalid();
    };

    handleUsernameView();
    handlePasswordView();

    usernameView.element.addEventListener("input", handleUsernameView);
    passwordView.element.addEventListener("input", handlePasswordView);

    buttonElement.addEventListener("click", async () => {
        const username = handleUsernameView();
        const password = handlePasswordView();

        if (username === undefined || password === undefined)
            return;

        formView.redrawRunning();

        const ok = await authorize(username, password);

        if (!ok) {
            formView.redrawByUnknownError();
            alert(text.unknownErrorMessage);
            return;
        }

        window.location.assign(locations.waterBalanceMenu);
    });
}

export function constructSignOutFormControllers(
    buttonElement: HTMLElement,
): void {
    buttonElement.addEventListener("onclick", () => {
        logout();
        window.location.assign(locations.authorization);
    })
}

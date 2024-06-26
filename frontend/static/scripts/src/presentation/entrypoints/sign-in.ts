import { constructAuthorizationFormControllers } from "../controllers/access.js";
import { FormFieldView, FormView } from "../views/forms.js";

constructAuthorizationFormControllers(
    new FormView(<HTMLDivElement>document.querySelector("#authorization-form")),
    new FormFieldView(
        <HTMLInputElement>document.querySelector("#input-name"),
        "valid-form-field",
    ),
    new FormFieldView(
        <HTMLInputElement>document.querySelector("#input-password"),
        "valid-form-field",
    ),
    <HTMLButtonElement>document.querySelector("#sign-in-button"),
);

import * as authorizationForm from "../controllers/authorization-form.js";

authorizationForm.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLInputElement>document.querySelector("#input-password"),
    <HTMLButtonElement>document.querySelector("#sign-in-button"),
)

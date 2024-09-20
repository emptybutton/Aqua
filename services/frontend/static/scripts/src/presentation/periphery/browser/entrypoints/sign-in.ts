import * as form from "../controllers/forms/login-form.js";

form.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLInputElement>document.querySelector("#input-password"),
    <HTMLDivElement>document.querySelector("#notification"),
    <HTMLDivElement>document.querySelector("#notification-text"),
    <HTMLImageElement>document.querySelector("#notification-close-button"),
    <HTMLButtonElement>document.querySelector("#sign-in-button"),
);

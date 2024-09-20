import * as form from "../controllers/login-form.js";

form.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLInputElement>document.querySelector("#input-password"),
    <HTMLDivElement>document.querySelector(".default-neutral-notification"),
    <HTMLDivElement>document.querySelector(".default-notification-text"),
    <HTMLImageElement>document.querySelector(".default-notification-close-button"),
    <HTMLButtonElement>document.querySelector("#sign-in-button"),
);

import * as form from "../controllers/registration-form.js";

form.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLDivElement>document.querySelector(".default-neutral-notification"),
    <HTMLDivElement>document.querySelector(".default-notification-text"),
    <HTMLImageElement>document.querySelector(".default-notification-close-button"),
);

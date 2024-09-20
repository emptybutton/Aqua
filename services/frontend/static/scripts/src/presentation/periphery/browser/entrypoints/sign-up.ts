import * as form from "../controllers/forms/registration-form.js";

form.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLInputElement>document.querySelector("#input-password"),
    <HTMLInputElement>document.querySelector("#input-weight-kilograms"),
    <HTMLInputElement>document.querySelector("#target-water-balance-milliliters"),
    <HTMLDivElement>document.querySelector("#notification"),
    <HTMLDivElement>document.querySelector("#notification-text"),
    <HTMLImageElement>document.querySelector("#notification-close-button"),
);

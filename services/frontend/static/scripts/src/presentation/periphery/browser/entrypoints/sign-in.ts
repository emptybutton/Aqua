import * as loginForm from "../controllers/login-form.js";

loginForm.constructControllers(
    <HTMLInputElement>document.querySelector("#input-name"),
    <HTMLInputElement>document.querySelector("#input-password"),
    <HTMLDivElement>document.querySelector("#notification"),
    <HTMLButtonElement>document.querySelector("#sign-in-button"),
    <HTMLImageElement>document.querySelector("#close-button"),
);

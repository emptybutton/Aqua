import { constructSignOutFormControllers } from "../controllers/access.js";
import * as locations from "../views/locations.js";
import { authorizationCompleted } from "../../services/access.js";

if (!authorizationCompleted())
    window.location.assign(locations.authorization);

constructSignOutFormControllers(
    <HTMLButtonElement>document.querySelector("#sign-out-button"),
);

import * as locations from "../views/locations.js";
import { authorizationCompleted } from "../../services/access.js";

if (!authorizationCompleted())
    window.location.assign(locations.authorization);

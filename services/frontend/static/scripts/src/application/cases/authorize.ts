import { Password, Username, maybe, StrongPasswordPower } from "../../domain/value_objects.js";
import * as gateways from "../ports/gateways.js";
import * as views from "../ports/views.js";
import * as loggers from "../ports/loggers.js";
import * as repos from "../ports/repos.js";
import * as storages from "../ports/storages.js";

export async function perform(
    usernameText: string,
    passwordText: string,
    backendGateway: gateways.BackendGateway,
    logger: loggers.Logger,
    usernameView: views.TernaryView,
    passwordView: views.TernaryView,
    usernamesOfUnregisteredUsers: repos.Usernames,
    jwtStorage: storages.JWTStorage,
): Promise<void> {
    let username = maybe(() => new Username(usernameText));
    let password = Password.with(passwordText);

    if (username === undefined || password.power instanceof StrongPasswordPower)
        return;

    let result = await backendGateway.authorize(username, password);

    if (result === "backendIsNotWorking")
        logger.logBackendIsNotWorking();
    else if (result === "incorrectPassword")
        passwordView.redrawInvalid();
    else if (result === "noUser") {
        usernamesOfUnregisteredUsers.add(username);
        usernameView.redrawInvalid();
    }
    else {
        jwtStorage.jwt = result.jwt;
    }
}

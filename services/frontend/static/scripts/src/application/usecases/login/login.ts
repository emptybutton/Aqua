import * as clients from "../../ports/clients.js";
import * as views from "../../ports/views.js";
import * as loggers from "../../ports/loggers.js";
import * as repos from "../../ports/repos.js";
import * as _password from "../../../domains/access/value-objects/password.js";
import * as _username from "../../../domains/access/value-objects/username.js";
import * as _credentials from "../../../domains/access/value-objects/credentials.js";

export async function execute(
    usernameText: string,
    passwordText: string,
    backend: clients.Backend,
    logger: loggers.Logger,
    usernameView: views.OptionalPositiveView,
    passwordView: views.OptionalPositiveView,
    usernamesOfUnregisteredUsers: repos.Usernames,
    invalidCredentialSet: repos.CredentialSet,
    windowView: views.WindowView,
    notificationView: views.LoginNotificationView,
): Promise<void> {
    let username = _username.anyWith(usernameText);
    let password = _password.Password.with(passwordText);

    if (username instanceof _username.InvalidUsername) {
        notificationView.redrawInvalidUsername(username)
        return;
    }

    if (password.power instanceof _password.WeakPower) {
        notificationView.redrawInvalidPassword(password)
        return;
    }

    let credentials = new _credentials.Credentials(username, password);
    let result = await backend.login(credentials);

    if (result === "error") {
        await logger.logBackendIsNotWorking();
        notificationView.redrawTryAgainLater();
    }
    else if (result === "incorrectPassword") {
        if (usernamesOfUnregisteredUsers.contains(username))
            usernamesOfUnregisteredUsers.remove(username);

        invalidCredentialSet.add(credentials);
        notificationView.redrawInvalidCredentials(credentials);
        usernameView.redrawNeutral();
        passwordView.redrawNeutral();
    }
    else if (result === "noUser") {
        usernamesOfUnregisteredUsers.add(username);
        notificationView.redrawNoUserWithUsername(username);
        usernameView.redrawNeutral();
    }
    else {
        windowView.redrawForMainInteractions();
    }
}

import * as _views from "../ports/views.js";
import * as _repos from "../ports/repos.js";
import * as _timeouts from "../ports/timeouts.js";
import * as _clients from "../ports/clients.js";
import * as _loggers from "../ports/loggers.js";
import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";

export function prepareNewAccountUsername(
    usernameText: string,
    usernameView: _views.ValidationView,
    notificationView: _views.RegistrationNotificationView,
    usernamesOfRegisteredUsers: _repos.Usernames,
    usernamesOfUnregisteredUsers: _repos.Usernames,
    timeoutForUsernameAvailability: _timeouts.Timeout,
    backend: _clients.Backend,
    logger: _loggers.Logger,
): void {
    let username = _username.anyWith(usernameText);

    if (username instanceof _username.InvalidUsername) {
        notificationView.redrawForInvalidUsernameHint(username);
        usernameView.redrawNeutral();
        timeoutForUsernameAvailability.doNothing();

        return;
    }

    if (usernamesOfRegisteredUsers.contains(username)) {
        notificationView.redrawForTakenUsernameHint(username);
        usernameView.redrawNeutral();
        timeoutForUsernameAvailability.doNothing();

        return;
    }

    notificationView.redrawForValidUsernameHint(username);
    usernameView.redrawOk();

    if (usernamesOfUnregisteredUsers.contains(username)) {
        timeoutForUsernameAvailability.doNothing();
        return;
    }

    timeoutForUsernameAvailability.doAfter(2500, async () => {
        let result = await backend.existsNamed(username);

        if (result === "error") {
            logger.logBackendIsNotWorking();
            return;
        }

        if (result.exists) {
            usernamesOfRegisteredUsers.add(username);
            notificationView.redrawUsernameTaken(username);
            usernameView.redrawNeutral();
        }
        else
            usernamesOfUnregisteredUsers.add(username);
    });
}

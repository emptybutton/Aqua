import * as views from "../ports/views.js";
import * as repos from "../ports/repos.js";
import * as _username from "../../domain/value-objects/username.js";
import * as _password from "../../domain/value-objects/password.js";
import * as _credentials from "../../domain/value-objects/credentials.js";

export async function prepareToLogin(
    usernameText: string,
    passwordText: string,
    usernameView: views.ValidationView,
    passwordView: views.ValidationView,
    usernamesOfUnregisteredUsers: repos.Usernames,
    invalidCredentialSet: repos.CredentialSet,
    notificationView: views.LoginNotificationView,
): Promise<void> {
    let username = _username.anyWith(usernameText);
    let password = _password.Password.with(passwordText);
    let credentials = new _credentials.Credentials(username, password);

    if (invalidCredentialSet.contains(credentials)) {
        notificationView.redrawLastTimeThereWasNoUserWithCredentials(credentials);
        usernameView.redrawNeutral();
        passwordView.redrawNeutral();
        return;
    }

    let wasNotificationViewRedrawn = false;

    if (username instanceof _username.InvalidUsername) {
        notificationView.redrawInvalidUsername(username);
        wasNotificationViewRedrawn = true;
        usernameView.redrawNeutral();
    }
    else if (usernamesOfUnregisteredUsers.contains(username)) {
        notificationView.redrawLastTimeThereWasNoUserNamed(username);
        wasNotificationViewRedrawn = true;
        usernameView.redrawNeutral();
    }
    else
        usernameView.redrawOk();

    if (password.power instanceof _password.WeakPower) {
        notificationView.redrawInvalidPassword(password);
        wasNotificationViewRedrawn = true;
        passwordView.redrawNeutral();
    }
    else
        passwordView.redrawOk();

    if (!wasNotificationViewRedrawn) {
        notificationView.redrawInvisible();
    }
}

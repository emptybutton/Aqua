import * as views from "../../ports/views.js";
import * as repos from "../../ports/repos.js";
import * as _username from "../../../domains/access/value-objects/username.js";
import * as _password from "../../../domains/access/value-objects/password.js";
import * as _credentials from "../../../domains/access/value-objects/credentials.js";

export enum Priority { forUsername, forPassword }

export class BaseError extends Error {}

export class InvalidPriorityError extends BaseError {}

export async function execute(
    usernameText: string,
    passwordText: string,
    priority: Priority,
    usernameView: views.OptionalPositiveView,
    passwordView: views.OptionalPositiveView,
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

    const validateUsername = () => _validateUsername(
        username, notificationView, usernameView, usernamesOfUnregisteredUsers
    )
    const validatePassword = () => _validatePassword(
        password, passwordView, notificationView
    )

    let ok: boolean;

    if (priority === Priority.forUsername)
        ok = validateUsername() && validatePassword();
    else if (priority === Priority.forPassword)
        ok = validatePassword() && validateUsername();
    else
        throw new InvalidPriorityError();

    if (ok) {
        notificationView.redrawInvisible();
    }
}

function _validateUsername(
    username: _username.AnyUsername,
    notificationView: views.LoginNotificationView,
    usernameView: views.OptionalPositiveView,
    usernamesOfUnregisteredUsers: repos.Usernames,
): boolean {
     if (username instanceof _username.InvalidUsername) {
        notificationView.redrawInvalidUsername(username);
        usernameView.redrawNeutral();
        return false;
    }
    else if (usernamesOfUnregisteredUsers.contains(username)) {
        notificationView.redrawLastTimeThereWasNoUserNamed(username);
        usernameView.redrawNeutral();
        return false;
    }
    else {
        usernameView.redrawOk();
        return true;
    }
}

function _validatePassword(
    password: _password.Password,
    passwordView: views.OptionalPositiveView,
    notificationView: views.LoginNotificationView,
): boolean {
     if (password.power instanceof _password.WeakPower) {
        notificationView.redrawInvalidPassword(password);
        passwordView.redrawNeutral();
        return false;
    }

    passwordView.redrawOk();
    return true;
}

import * as views from "../ports/views.js";
import * as repos from "../ports/repos.js";
import * as _username from "../../domain/value-objects/username.js";
import * as _password from "../../domain/value-objects/password.js";
import * as _credentials from "../../domain/value-objects/credentials.js";

export enum Priority { forUsername, forPassword }

export class BaseError extends Error {}

export class InvalidPriorityError extends BaseError {}

export async function prepareToLogin(
    usernameText: string,
    passwordText: string,
    priority: Priority,
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
    usernameView: views.ValidationView,
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
    passwordView: views.ValidationView,
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

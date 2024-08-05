import { Password, Username, maybe, StrongPasswordPower } from "../../domain/value_objects.js";
import * as views from "../ports/views.js";
import * as repos from "../ports/repos.js";

export async function perform(
    usernameText: string,
    passwordText: string,
    usernameView: views.TernaryView,
    passwordView: views.TernaryView,
    usernamesOfUnregisteredUsers: repos.Usernames,
): Promise<void> {
    let username = maybe(() => new Username(usernameText));
    let password = Password.with(passwordText);

    if (username === undefined || usernamesOfUnregisteredUsers.contains(username))
        usernameView.redrawNeutral();
    else
        usernameView.redrawValid();

    if (password.power instanceof StrongPasswordPower)
        passwordView.redrawValid();
    else
        passwordView.redrawNeutral();
}

import * as repos from "../../application/ports/repos.js";
import * as _username from "../../domain/value-objects/username.js";
import * as _credentials from "../../domain/value-objects/credentials.js";

export class InMemoryUsernames implements repos.Usernames {
    private _usernameTexts: Set<string>;

    constructor(usernames: _username.Username[] = []) {
        this._usernameTexts = new Set(usernames.map(username => username.text));
    }

    add(username: _username.Username): void {
        this._usernameTexts.add(username.text);
    }

    contains(username: _username.Username): boolean {
        return this._usernameTexts.has(username.text);
    }

    remove(username: _username.Username): void {
        this._usernameTexts.delete(username.text);
    }
}

export class InMemoryCredentialSet implements repos.CredentialSet {
    private _passwordTextsByUsernameText: Record<string, Set<string>>;

    constructor(credentialsArray: _credentials.Credentials[] = []) {
        this._passwordTextsByUsernameText = {};

        credentialsArray.forEach(this.add);
    }

    add(credentials: _credentials.Credentials): void {
        let passwordTexts = this._passwordTextsByUsernameText[credentials.username.text];

        if (passwordTexts === undefined) {
            passwordTexts = new Set();
            this._passwordTextsByUsernameText[credentials.username.text] = passwordTexts;
        }

        passwordTexts.add(credentials.password.text);
    }

    contains(credentials: _credentials.Credentials): boolean {
        let passwordTexts = this._passwordTextsByUsernameText[credentials.username.text];

        if (passwordTexts === undefined)
            return false;

        return passwordTexts.has(credentials.password.text);
    }
}

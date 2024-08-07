import * as repos from "../../application/ports/repos.js";
import * as vos from "../../domain/value_objects.js";

export class InMemoryUsernames implements repos.Usernames {
    private _usernameTexts: Set<string>;

    constructor(usernames: vos.Username[] = []) {
        this._usernameTexts = new Set(usernames.map(username => username.text));
    }

    add(username: vos.Username): void {
        this._usernameTexts.add(username.text);
    }

    contains(username: vos.Username): boolean {
        return this._usernameTexts.has(username.text);
    }
}

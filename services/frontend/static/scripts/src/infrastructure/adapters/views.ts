import * as views from "../../application/ports/views.js";
import * as _username from "../../domains/access/value-objects/username.js";
import * as _password from "../../domains/access/value-objects/password.js";
import * as _credentials from "../../domains/access/value-objects/credentials.js";

export const pageView: views.WindowView = {
    redrawToLogin(): void {
        window.location.assign("/sign-in");
    },

    redrawForMainInteractions(): void {
        window.location.assign("/");
    },
}

export class ValidationCSSView implements views.ValidationView {
    constructor(
        private _element: HTMLElement,
        private _classNameWhenOk: string,
        private _classNameWhenNeutral: string,
    ) {}

    redrawOk(): void {
        this._element.className = this._classNameWhenOk;
    }

    redrawNeutral(): void {
        this._element.className = this._classNameWhenNeutral;
    }
}

export class LoginNotificationLayoutView implements views.LoginNotificationView {
    private _textElement: HTMLElement;

    constructor(private _notificationElement: HTMLElement) {
        if (_notificationElement.id !== "notification")
            throw new Error("`_notificationElement` must have id = \"notification\"");
        
        let textElement = _notificationElement.querySelector("#text");

        if (!(textElement instanceof HTMLElement))
            throw new Error("`_notificationElement` must have `#text` subelement");

        this._textElement = textElement;
    }

    redrawInvisible(): void {
        this._notificationElement.style.display = "none";
        this._textElement.innerText = "";
    }

    redrawNoUserWithUsername(_: _username.AnyUsername): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "bad-notification";
        this._textElement.innerText = "Пользователя с таким именем нет";
    }

    redrawInvalidCredentials(_: _credentials.Credentials): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "bad-notification";
        this._textElement.innerText = "Неправильный пароль";
    }

    redrawLastTimeThereWasNoUserNamed(_: _username.AnyUsername): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "neutral-notification";
        this._textElement.innerText = "В прошлых попытках пользователя с таким именем не было";
    }

    redrawLastTimeThereWasNoUserWithCredentials(_: _credentials.Credentials): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "neutral-notification";
        this._textElement.innerText = "В прошлых попытках такой пароль не подошёл";
    }

    redrawInvalidUsername(_: _username.AnyUsername): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "bad-notification";
        this._textElement.innerText = "Не может быть пользователя с таким именем";
    }

    redrawInvalidPassword(_: _password.Password): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "bad-notification";
        this._textElement.innerText = "Не может быть пользователя с таким паролем";
    }

    redrawTryAgainLater(): void {
        this._notificationElement.style.display = "unset";
        this._notificationElement.className = "bad-notification";
        this._textElement.innerText = "Что то пошло не по плану, попробуйте когда нибудь потом!";
    }
}

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

export class LoginDefaultNotificationCSSView implements views.LoginNotificationView {
    constructor(
        private _notificationElement: HTMLElement,
        private _textElement: HTMLElement,
    ) {}

    redrawInvisible(): void {
        this._notificationElement.style.display = "none";
        this._textElement.innerText = "";
    }

    redrawNoUserWithUsername(_: _username.AnyUsername): void {
        this._textElement.innerText = "Пользователя с таким именем нет";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawInvalidCredentials(_: _credentials.Credentials): void {
        this._textElement.innerText = "Неправильный пароль";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawLastTimeThereWasNoUserNamed(_: _username.AnyUsername): void {
        this._textElement.innerText = "В прошлых попытках пользователя с таким именем не было";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawLastTimeThereWasNoUserWithCredentials(_: _credentials.Credentials): void {
        this._textElement.innerText = "В прошлых попытках такой пароль не подошёл";
        this._redrawNeutral();
        this._redrawVisible();
    }

    redrawInvalidUsername(_: _username.AnyUsername): void {
        this._textElement.innerText = "Не может быть пользователя с таким именем";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawInvalidPassword(_: _password.Password): void {
        this._textElement.innerText = "Не может быть пользователя с таким паролем";
        this._redrawBad();
        this._redrawVisible();
    }

    redrawTryAgainLater(): void {
        this._textElement.innerText = "Что то пошло не по плану, попробуйте когда нибудь потом!";
        this._redrawBad();
        this._redrawVisible();
    }

    private _redrawVisible(): void {
        this._notificationElement.style.display = "unset";
    }

    private _redrawBad(): void {
        this._notificationElement.className = "default-bad-notification";
    }

    private _redrawNeutral(): void {
        this._notificationElement.className = "default-neutral-notification";
    }
}

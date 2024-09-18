import * as _timeouts from "../../application/ports/timeouts.js";

export class InMemoryTimeout implements _timeouts.Timeout {
    private _timeoutID: number | undefined = undefined;

    doAfter(milliseconds: number, action: () => never): void {
        if (this._timeoutID !== undefined)
            clearTimeout(this._timeoutID);

        let handler = () => {
            this._timeoutID = undefined;
            action();
        }

        this._timeoutID = setTimeout(handler, milliseconds);
    }

    doNothing(): void {
        if (this._timeoutID === undefined)
            return;

        clearTimeout(this._timeoutID);
        this._timeoutID = undefined;
    }
}

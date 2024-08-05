import * as loggers from "../../application/ports/loggers.js";

export const consoleLogger: loggers.Logger = {
    logBackendIsNotWorking(): void {
        console.error("backend is not working");
    },
}

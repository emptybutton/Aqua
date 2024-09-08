import * as loggers from "../../application/ports/loggers.js";

export const consoleLogger: loggers.Logger = {
    async logBackendIsNotWorking(): Promise<void> {
        console.error("backend is not working");
    },
}

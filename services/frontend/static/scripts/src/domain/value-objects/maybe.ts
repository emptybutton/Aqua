import { VOError } from "./error.js";

export function maybe<T>(factory: () => T): T | undefined {
    try {
        return factory()
    } catch (error) {
        if (error instanceof VOError)
            return undefined;

        throw error;
    }
}

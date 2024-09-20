export function parseOptional(text: string): number | undefined {
    return text === '' ? undefined : parseFloat(text);
}

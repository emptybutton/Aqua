from secrets import token_hex

from auth.application.ports import generators


class GenerateByTokenHex(generators.GenerateHighEntropyText):
    def __call__(self) -> str:
        return token_hex()

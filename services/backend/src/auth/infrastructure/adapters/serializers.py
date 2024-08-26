import hashlib

from auth.application.ports import serializers
from auth.domain import value_objects as vos


class SHA256PasswordHasher(
    serializers.AsymmetricSerializer[vos.Password, vos.PasswordHash],
):
    def serialized(self, password: vos.Password) -> vos.PasswordHash:
        hash_object = hashlib.sha256()
        hash_object.update(password.text.encode("utf-8"))

        return vos.PasswordHash(text=hash_object.hexdigest())


class ConcatenatingPasswordHasher(
    serializers.AsymmetricSerializer[vos.Password, vos.PasswordHash],
):
    def serialized(self, password: vos.Password) -> vos.PasswordHash:
        return vos.PasswordHash(text=f"{password.text}_hash")

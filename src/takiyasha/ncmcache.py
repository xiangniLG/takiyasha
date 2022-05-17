from __future__ import annotations

from io import BytesIO
from typing import IO

from .common import Crypter, KeylessCipher
from .utils import FileThing, is_filepath, verify_fileobj_readable, verify_fileobj_seekable

__all__ = ['NCMCache', 'NCMCacheCipher']


class NCMCacheCipher(KeylessCipher):
    def decrypt(self, cipherdata: bytes, start_offset: int = 0) -> bytes:
        bool(start_offset)
        return bytes(b ^ 163 for b in cipherdata)


class NCMCache(Crypter):
    def __init__(self, filething: FileThing | None = None):
        if filething is None:
            self._raw = BytesIO()
            self._cipher: NCMCacheCipher = NCMCacheCipher()
            self._name: str | None = None
        else:
            super().__init__(filething)

    def load(self, filething: FileThing) -> None:
        if is_filepath(filething):
            fileobj: IO[bytes] = open(filething, 'rb')  # type: ignore
            self._name = fileobj.name
        else:
            fileobj: IO[bytes] = filething  # type: ignore
            self._name = None
            verify_fileobj_readable(fileobj, bytes)
            verify_fileobj_seekable(fileobj)

        self._raw = BytesIO(fileobj.read())
        if is_filepath(filething):
            fileobj.close()
        self._cipher: NCMCacheCipher = NCMCacheCipher()

    @property
    def cipher(self) -> NCMCacheCipher:
        return self._cipher

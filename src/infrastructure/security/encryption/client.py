import binascii
import hashlib

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Util.Padding import unpad

from src.configuration import settings

from .collections import ClientDisabled


class Encryption:
    @property
    def hash(self) -> bytes:
        return hashlib.sha256(settings.CRYPTOGRAPHY_SECRET_KEY.encode()).digest()

    def encrypt(self, data: str) -> str:
        if not settings.CRYPTOGRAPHY:
            raise ClientDisabled

        cipher = AES.new(self.hash[:16], AES.MODE_CBC, self.hash[16:32])

        return binascii.hexlify(cipher.encrypt(pad(data.encode(), AES.block_size))).decode()

    def decrypt(self, data: str) -> str:
        if not settings.CRYPTOGRAPHY:
            raise ClientDisabled

        cipher = AES.new(self.hash[:16], AES.MODE_CBC, self.hash[16:32])

        return unpad(cipher.decrypt(binascii.unhexlify(data)), AES.block_size).decode()

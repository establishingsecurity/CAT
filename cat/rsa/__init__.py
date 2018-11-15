from typing import Callable, NewType

from gmpy2 import mpz
from Crypto.PublicKey import RSA

from .attacks import lsb_oracle


RSACiphertext = NewType('RSACiphertext', int)
RSAPlaintext = NewType('RSAPlaintext', int)


RSAKey = NewType('RSAKey', RSA)


class RSA():
    def add_lsb_oracle(self, oracle):
        # type: Callable[[RSACiphertext], bool]
        self.lsb_oracle = oracle

    def run_lsb_oracle(self, ciphertext):
        # type: RSACiphertext
        return int(self.lsb_oracle(self.pk, ciphertext, self.oracle))


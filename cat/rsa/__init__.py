from typing import Callable, NewType

from gmpy2 import mpz

from .attacks import lsb_oracle


RSACiphertext = NewType('RSACiphertext', int)
RSAPlaintext = NewType('RSAPlaintext', int)


class RSAPublicKey():
    def __init__(self, n: int, e: int):
        self.n = mpz(n)
        self.e = mpz(e)

class RSAPrivateKey():
    def __init__(self, n: int, d: int):
        self.n = mpz(n)
        self.d = mpz(d)


class RSA():
    def add_lsb_oracle(self, oracle):
        # type: Callable[[RSACiphertext], bool]
        self.lsb_oracle = oracle

    def run_lsb_oracle(self, ciphertext):
        # type: RSACiphertext
        return int(self.lsb_oracle(self.pk, ciphertext, self.oracle))


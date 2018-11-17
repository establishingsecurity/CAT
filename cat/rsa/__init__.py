import itertools
from typing import Callable, NewType, List

from gmpy2 import mpz
from Cryptodome.PublicKey import RSA

from .attacks import lsb_oracle
from .util import reconstruct_private


RSACiphertext = NewType('RSACiphertext', int)
RSAPlaintext = NewType('RSAPlaintext', int)


RSAKey = NewType('RSAKey', RSA)


class RSA():
    def __init__(self):
        self._keys = []
        self._factors = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys):
        # type: List[RSAKey]
        # Test if we already have factors of the public keys
        self._keys = [
                reconstruct_private(key, p) if key % p == 0 else key
                for (key, p) in itertools.product(keys, self._factors)
        ]

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, factors):
        # type: List[mpz]
        # Test if we got new immediatly useful factors of public key
        self._factors = factors
        self._keys = [
                reconstruct_private(key, p) if key % p == 0 else key
                for (key, p) in itertools.product(self._keys, self._factors)
        ]

    def add_lsb_oracle(self, oracle):
        # type: Callable[[RSACiphertext], bool]
        self.lsb_oracle = oracle

    def run_lsb_oracle(self, ciphertext):
        # type: RSACiphertext
        """
        This function implements an attack against RSA oracles that return the least
        significant bit or parity of the decrypted ciphertext.
        It is able to decrypt a single message that has to be valid.

        Runs against the first key in the list
        """
        # TODO: Detect the right public key
        return int(self.lsb_oracle(self._keys[0], ciphertext, self.oracle))


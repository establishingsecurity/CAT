import itertools
from typing import Callable, NewType, List

from gmpy2 import mpz
from Cryptodome.PublicKey import RSA

from . import util
from .attacks import lsb_oracle


RSACiphertext = NewType('RSACiphertext', int)
RSAPlaintext = NewType('RSAPlaintext', int)


RSAKey = NewType('RSAKey', RSA)


class RSADriver():
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
        self._keys = util.reconstruct_privates(keys, self._factors)
        print(self._keys)

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, factors):
        # type: List[mpz]
        # Test if we got new immediatly useful factors of public key
        self._factors = factors
        self._keys = util.reconstruct_privates(self._keys, factors)

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
        return int(lsb_oracle(self._keys[0], ciphertext, self.lsb_oracle))


import itertools
from typing import Callable, List, NewType

from Cryptodome.PublicKey import RSA
from gmpy2 import mpz

from . import util
from .attacks import lsb_oracle

import logging


from cat.log.log import LIB_ROOT_LOGGER_NAME as LOGGER

RSACiphertext = int
RSAPlaintext = int

RSAKey = RSA.RsaKey


class RSADriver:
    def __init__(self):
        self._keys = []
        self._factors = []

    @property
    def keys(self):
        return self._keys

    @keys.setter
    def keys(self, keys):
        # type: (List[RSAKey]) -> None
        # Test if we already have factors of the public keys
        self._keys = util.reconstruct_privates(keys, self._factors)
        if self._keys != keys:
            logger = logging.getLogger(LOGGER)
            logger.info("Recovered more keys with known factors")

    @property
    def factors(self):
        return self._factors

    @factors.setter
    def factors(self, factors):
        # type: (List[mpz]) -> None
        # Test if we got new immediatly useful factors of public key
        self._factors = factors
        self._keys = util.reconstruct_privates(self._keys, factors)

    def add_lsb_oracle(self, oracle):
        # type: (Callable[[RSACiphertext], bool]) -> None
        self.lsb_oracle = oracle

    def run_lsb_oracle(self, ciphertext):
        # type: (RSACiphertext) -> int
        """
        This function implements an attack against RSA oracles that return the least
        significant bit or parity of the decrypted ciphertext.
        It is able to decrypt a single message that has to be valid.

        Runs against the first key in the list
        """
        # TODO: Detect the right public key
        return int(lsb_oracle(self._keys[0], ciphertext, self.lsb_oracle))

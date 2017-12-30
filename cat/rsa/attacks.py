from Cryptodome.PublicKey import RSA
from gmpy2 import mpz, invert, powmod

from .. import Oracle

class LSBOracle(Oracle):
    """
    This class implements an attack against RSA oracles that return the least
    significant bit of the decrypted ciphertext.
    It is able to decrypt a single message. This message has to be valid.

    To instantiate it, implement the query method taking an integer and
    returning the least significant bit returned by the oracle
    """

    # TODO: Type this
    def __init__(self, pk, message: int):
        self.pk = pk
        self.t = mpz(message)
        self.mult = invert(2, self.pk.n)

    def run(self) -> int:
        m = 0

        for i in range(1, self.pk.n.bit_length() +1):
            # Encrypt multiplicator
            mult = powmod(self.mult * i, self.pk.e, self.pk.n)
            # Forge query message
            c = self.t * mult

            # Get lsb of forged message
            m += (self.query(c) << (i-1))

        return m







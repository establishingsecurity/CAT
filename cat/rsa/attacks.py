from Cryptodome.PublicKey import RSA
from gmpy2 import mpz, mpfr, invert, powmod
import decimal

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
        self.mult = powmod(2, self.pk.e, self.pk.n)

    def run(self) -> int:
        t = mpz((self.t*self.mult) % self.pk.n)
        lower = mpfr(0)
        upper = mpfr(self.pk.n)
        for i in range(self.pk.n.bit_length()):
            possible_plaintext = (lower + upper)/2
            if not self.query(t):
                upper = possible_plaintext            # plaintext is in the lower half
            else:
                lower = possible_plaintext            # plaintext is in the upper half
            t=(t*self.mult) % self.pk.n
        return int(upper)







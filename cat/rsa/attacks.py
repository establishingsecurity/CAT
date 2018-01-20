from Cryptodome.PublicKey import RSA
from gmpy2 import mpz, mpfr, invert, powmod, gcd, isqrt, is_square

from .. import Oracle

def reconstruct_private(pk, p):
    """
    Reconstructs the private key from a public key and a factor of the modulus
    """
    q = pk.n // p
    assert p*q == pk.n
    phi = (p-1)*(q-1)
    d = int(invert(pk.e, (p-1)*(q-1)))
    assert pk.e * d % phi == 1
    return RSA.construct((pk.n, pk.e, d, p, q), consistency_check=True)


def fermat_factoring(pk):
    """
    This attack tries to factor moduli with primes that are close to each other
    and returns a matching rsa private key

    >>> from gmpy2 import next_prime
    >>> p = int(next_prime(2**511))
    >>> q = int(next_prime(p))
    >>> e = 2**16 + 1
    >>> pk = RSA.construct((p*q, e))
    >>> key = reconstruct_private(pk, p)
    >>> sk = fermat_factoring(pk)
    >>> plain = 256
    >>> cipher = powmod(plain, key.e, key.n)
    >>> plain == int(powmod(cipher, sk.d, sk.n))
    True
    """
    # This is not correct, what we want is ceil(sqrt(pk.n))
    a = isqrt(pk.n)
    bsqr = a*a - pk.n
    while not is_square(bsqr):
        a = a + 1
        bsqr = a*a - pk.n

    return reconstruct_private(pk, int(a - isqrt(bsqr)))


def common_divisor(pk, product: int):
    """
    This attack takes an rsa public key and some integer that is known to have a
    common divisor with the modulus and returns a matching rsa private key

    >>> key = RSA.generate(2048)
    >>> sk = common_divisor(key.publickey(), key.p * 17)
    >>> plain = 256
    >>> cipher = powmod(plain, key.e, key.n)
    >>> plain == int(powmod(cipher, sk.d, sk.n))
    True
    """
    p = int(gcd(mpz(pk.n), mpz(product)))
    return reconstruct_private(pk, p)


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







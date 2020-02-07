from typing import TYPE_CHECKING, Callable

from Cryptodome.PublicKey import RSA
from gmpy2 import floor, gcd, invert, is_square, isqrt, mpfr, mpz, powmod

from .util import reconstruct_private

from cat.factorize.fermat import factor

if TYPE_CHECKING:
    from . import RSAKey, RSACiphertext, RSAPlaintext

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

    return reconstruct_private(pk, int(factor(pk.n)))


def common_divisor(pk, product):
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


def lsb_oracle(public_key, ciphertext, oracle):
    # type: (RSAKey, RSACiphertext, Callable[[RSACiphertext], bool]) -> RSAPlaintext
    r"""
    The Least Significant Bit Oracle attack is a simpler variation on
    Bleichenbacher.
    
    It assumes a decryption oracle :math:`LSB(\dot)` that accepts ciphertexts and returns the
    least significant or parity bit of the decrypted plaintext.
    """
    mult = powmod(2, public_key.e, public_key.n)

    t = (ciphertext * mult) % public_key.n
    lower = mpfr(0)
    upper = mpfr(public_key.n)
    for i in range(public_key.n.bit_length()):
        possible_plaintext = (lower + upper) / 2
        if not oracle(int(t)):
            upper = possible_plaintext  # plaintext is in the lower half
        else:
            lower = possible_plaintext  # plaintext is in the upper half
        t = (t * mult) % public_key.n
    return mpz(floor(upper))
